#!/bin/bash
# Abort in case of an error
set -e

DIR=$(dirname $(realpath $0))
BACKEND="$DIR/tagforestrest"
FRONTEND="$DIR/tagforest-frontend-vue"
DEPLOY_FRONTEND=true
DEPLOY_BACKEND=true
UPDATE_GIT=false
REPLACE_VERSION=false

usage() {
  cat << ENDUSAGE
Usage: $0 [-hbfgv] BRANCH
   -h              Show help
   -b              Deploy only backend
   -f              Deploy only frontend
   -g              Update and reset git repo
   -v              Replace version and date
ENDUSAGE
1>&2;
}

while getopts "hbfgv" opt; do
  case "${opt}" in
    h )
        usage
        exit 1;
        ;;
    b )
				DEPLOY_FRONTEND=false
        ;;
    f )
				DEPLOY_BACKEND=false
        ;;
    g )
				UPDATE_GIT=true
        ;;
    v )
				REPLACE_VERSION=true
        ;;
    * )
        usage
        exit 1;
      ;;
  esac
done

shift $((OPTIND-1))

BRANCH=main
if [ -n "$1" ]; then
  BRANCH=$1
fi

CONF="/etc/tagforest/config"
echo "Parsing $CONF";
eval "$(python << EOF
import configparser
config = configparser.RawConfigParser()
config.read('$CONF')
print((
    "BACKEND_DEPLOY_DIR={}\n" +
    "FRONTEND_DEPLOY_DIR={}\n"
    ).format(
    config['Django']['deploy-directory'],
    config['Vue']['deploy-directory'],
    ))
EOF
)";

if $UPDATE_GIT; then
  echo "Updating git";
  cd $DIR;
  # Pull the repository
  git fetch origin;
  git reset --hard && git clean -xf;
  git checkout -B $BRANCH;
  git reset --hard origin/$BRANCH;
fi

if $REPLACE_VERSION; then
  cd $DIR;
  echo "Update website's version and date";
  # Update version info in templates
  VERSION=$(git describe --tags)
  DATE=$(date +%D)
  ESCAPED_DATE=$(printf '%s\n' "$DATE" | sed -e 's/[\/&]/\\&/g')
  # Cut the string to avoid the script replacing itself
  VERSION_PLACEHOLDER="<\!--""CURRENT_VERSION-->"
  DATE_PLACEHOLDER="<\!--""CURRENT_VERSION_DATE-->"
  egrep -lRZ $VERSION_PLACEHOLDER . | xargs -0 -l sed -i -e "s/$VERSION_PLACEHOLDER/$VERSION/g";
  egrep -lRZ $DATE_PLACEHOLDER . | xargs -0 -l sed -i -e "s/$DATE_PLACEHOLDER/$ESCAPED_DATE/g";
fi

if $DEPLOY_BACKEND; then

	cd $BACKEND;
	echo "Copying to deploy directory";
	# Update tag app
	rsync -ah --delete --info=progress2 ./ $BACKEND_DEPLOY_DIR/;
	#rsync -ah --delete --info=progress2 locale/ $BACKEND_DEPLOY_DIR/locale;
	mv $BACKEND_DEPLOY_DIR/tagforestrest/server-settings.py $BACKEND_DEPLOY_DIR/tagforestrest/settings.py;

	cd $BACKEND_DEPLOY_DIR;

	echo "Making migrations and compiling messages";
	# Make migrations, compile messages
	source env/bin/activate;
	python manage.py makemigrations;
	python manage.py migrate;
	python manage.py compilemessages;
	python manage.py collectstatic;
	deactivate;

	cd $BACKEND;

	git reset --hard;

	echo "Restarting gunicorn";
	sudo systemctl restart gunicorn
fi

if $DEPLOY_FRONTEND; then
  cd $FRONTEND;
  cp src/constants.js.server src/constants.js;
  npm install;
  npx vue-cli-service build;
  rsync -ah --delete --info=progress2 dist/ $FRONTEND_DEPLOY_DIR/;
fi
