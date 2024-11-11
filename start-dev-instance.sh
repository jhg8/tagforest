#!/bin/bash

set -x

DIR=$(dirname $(realpath $0))

tmux new-session -d -s tagforest "\
  cd $DIR/tagforestrest ;\
  source env/bin/activate ;\
  python manage.py runserver 0.0.0.0:8000 ;\
  bash"

tmux set-window-option -g mode-keys vi
tmux rename-window 'INSTANCE'
tmux select-window -t tagforest:0

tmux split-window -h "\
  cd $DIR/tagforest-frontend-vue ;\
  npm run serve ;\
  bash"

tmux new-window "cd $DIR ; bash"
tmux rename-window 'DEV'
tmux select-window -t tagforest:1
tmux -2 attach-session -t tagforest
