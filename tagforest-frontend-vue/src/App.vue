<template>
  <nav><div class="container">
      <router-link to="/">Tagforest</router-link>
      <router-link v-if="!loggedIn" to="/auth">Login / register</router-link>
      <router-link v-else to="/profile">{{ loggedUser }}</router-link>
      <router-link to="/export">Import / Export</router-link>
      <router-link to="/about">About</router-link>
  </div></nav>
  <div id="content" >
  <router-view/>
  </div>
  <footer><div class="container">
    Version <!--CURRENT_VERSION--> (<!--CURRENT_VERSION_DATE-->)
  </div></footer>
</template>

<style lang="scss">

$yellow: #ffe167;
$lightpurple: #7545fe;
$purple: #642efe;
$white: #ffffff;
$lighterergrey: #efe8ff;
$lightergrey: #dcd6eb;
$lightgrey: #b8afd1;
$grey: #2c3e50;
$darkgrey: #232021;

html, body {
  margin: 0;
  padding: 0;
  height: 100%;
  min-width: 100vw;
}
@media all and (max-width: 800px) {
  html {
    font-size: 14px;
  }
}
@media all and (max-width: 600px) {
  html {
    font-size: 12px;
  }
}
@media all and (max-width: 400px) {
  html {
    font-size: 10px;
  }
}


#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: $grey;

	position: relative; /* needed for footer positioning*/
	margin: 0 auto; /* center, not in IE5 */
	height: auto !important; /* real browsers */
	height: 100%; /* IE6: treaded as min-height*/
	min-height: 100%; /* real browsers */
}

#content {
  padding-bottom: 13rem; /* bottom padding for footer */
}

button, input[type="submit"] {
  background-color: white;
  border: 1px solid $lightgrey;
  border-radius: 0.2em;
  padding: 0.5em;
  margin-right: 1em;
  cursor: pointer;
  color: $darkgrey;
}

form.textForm {
  margin-bottom: 3em;
  input[type="text"], input[type="password"] {
    width: 100%;
    border: none;
    border-bottom: 1px solid $lightgrey;
    padding: 0.3em;
    &:focus {
      border: none;
      outline: 0;
      border-bottom: 1px solid $lightgrey;
      font-size: 0.9em;
      box-shadow: 0 0 1em rgba(0, 0, 0, 0.1);
    }
  }
  span.text {
    display: block;
    overflow: hidden;
    padding-right: 10px;
    height: 3em;
    width: 32em;
  }
  span.textarea {
    display: block;
    overflow: hidden;
    padding-right: 10px;
    height: 20em;
    margin-bottom: 2em;
  }
  span.select {
    display: block;
    overflow: visible;
    padding-right: 10px;
  }
  label {
    display: block;
    padding-top: 0.2em;
    padding-right: 1em;
    float: bottom;
    text-align: right;
  }
  textarea {
    height: 20em;
    width: 100%;
    border: none;
    border-bottom: 1px solid $lightgrey;
    padding: 0.3em;
    overflow: none;
  }
  textarea:focus {
    border: none;
    outline: 0;
    border-bottom: 1px solid $lightgrey;
    box-shadow: 0 0 1em rgba(0, 0, 0, 0.1);
  }
  .formGrid {
    display: grid;
    grid-template-columns: max-content max-content;
    grid-gap: 1em;
  }
  input[type="text"] {
    width: 100%;
    border: none;
    border-bottom: 1px solid $lightgrey;
    padding: 0.3em;
  }
  input[type="text"]:focus {
    border: none;
    outline: 0;
    border-bottom: 1px solid $lightgrey;
    font-size: 0.9em;
    box-shadow: 0 0 1em rgba(0, 0, 0, 0.1);
  }
  input[type="submit"], button {
    margin-top: 2em;
  }
}

.popup, .popupExport {
  position: fixed;
  z-index: 1;
  left: 0;
  top: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  .container {
    background-color: $white;
    border-radius: 1em;
    padding: 1em;
    margin: 30vh auto;
    box-shadow: 0 0 1em rgba(0, 0, 0, 0.4);
    max-width: 40em;
    span.textarea {
      display: block;
      padding-right: 10px;
      margin-bottom: 2em;
    }
    textarea {
      overflow: scroll;
    }
  }
}

.popupExport {
  .container {
    padding: 1em;
    margin: 10vh auto;
    box-shadow: 0 0 1em rgba(0, 0, 0, 0.4);
    max-width: 60em;
    span.textarea {
      padding-right: 10px;
      height: 50vh;
      margin-bottom: 0;
    }
    textarea {
      height: 50vh;
      margin-bottom: 0;
    }
  }
}

nav {
  background-color: $purple;
  .container {
    text-align: center;
		padding-top: 2em;
		padding-bottom: 2em;
    a {
      padding: 1em;
      display: inline-block;
      font-weight: bold;
      color: $white;
      text-decoration: none;

      &.router-link-exact-active {
        color: $yellow;
      }
    }
  }
}

footer {
  background-color: $purple;
  color: $white;
  margin: 0;
  text-align: center;

  bottom: 0;
  position: absolute;
  width: 100%;
  min-height: 9rem;
  padding-top: 1em;
}

.container {
  max-width: 50rem;
  margin: auto;
}

section {
  .container {
    padding-top: 1em;
  }
}

section {
  .container {
    padding-top: 1em;
  }
  &.entry, &.tag {
    a {
      color: $white;
      font-weight: bold;
      background-color: $purple;
      border-radius: 0.2em;
      padding: 2em;
      padding-top: 0.5em;
      padding-left: 0.6em;
      text-decoration: none;
      vertical-align: middle;
      display: inline-block;
      margin-right: 0.5em;
      margin-bottom: 0.5em;
      &:hover {
        color: $yellow;
        background-color: $lightpurple;
      }
    }
  }
  &.tag {
    a {
      color: $grey;
      font-weight: normal;
      background-color: $white;
      border: 1px solid $grey;
      padding-right: 1em;
      padding-top: 0.5em;
      padding-bottom: 0.5em;
      padding-left: 0.6em;
      &:hover {
        color: $grey;
        background-color: $lightergrey;
      }
    }
  }
  &.control-tag, &.control-category {
    a {
      border: 1px solid $grey;
      background-color: $white;
      font-weight: normal;
      color: $grey;
      border-radius: 1em;
      padding: 0.5em;
      padding-bottom: 0.3em;
      padding-right: 0.5em;
      padding-left: 0.6em;
      text-decoration: none;
      vertical-align: middle;
      display: inline-block;
      margin-right: 0.5em;
      margin-bottom: 0.5em;
      &:hover {
        background-color: $lightergrey;
      }
      &.active {
        background-color: $lightergrey;
      }
    }
  }
  &.control-category {
    a {
      border-radius: 0.2em;
    }
  }
}

pre {
  white-space: pre-wrap;       /* Since CSS 2.1 */
  white-space: -moz-pre-wrap;  /* Mozilla, since 1999 */
  white-space: -pre-wrap;      /* Opera 4-6 */
  white-space: -o-pre-wrap;    /* Opera 7 */
  word-wrap: break-word;       /* Internet Explorer 5.5+ */
}

label.edit-checkbox {
	.label {
		display: inline-block;
		border-radius: 0.4em;
		padding: 0.4em;
		cursor: pointer;
    background-color: $white;
    border: 1px solid $lightergrey;
	}
	input {
		opacity: 0;
		width: 0;
		height: 0;
    margin: 0;
	}
	input:checked + .label {
		background-color: $lighterergrey;
	}
	input:focus + .label {
		outline: 2px solid black;
	}
}

.control-buttons {
  button {
    color: $grey;
    background-color: $white;
    border: 1px solid $lightergrey;
    padding: 0;
    font: inherit;
    cursor: pointer;
		border-radius: 0.4em;
		padding: 0.4em;
  }
  label, button {
    margin-right: 1em;
  }
}

// @link https://moderncss.dev/pure-css-custom-checkbox-style/
.entry-checkbox, .tag-checkbox {
  display:inline-block;
	label {
		line-height: 1.1;
		display: grid;
		grid-template-columns: 1em auto;
		gap: 0.5em;
		cursor: pointer;
		color: $white;
		font-weight: bold;
		background-color: $purple;
		border-radius: 0.2em;
		padding: 2em;
		padding-top: 0.5em;
		padding-left: 0.5em;
		padding-left: 0.6em;
		text-decoration: none;
		vertical-align: middle;
		margin-right: 0.5em;
		margin-bottom: 0.5em;
    &:hover {
      color: $yellow;
    }
	}

	input[type="checkbox"] {
		/* Add if not using autoprefixer */
		-webkit-appearance: none;
		/* Remove most all native input styles */
		appearance: none;
		/* For iOS < 15 */
		background-color: var(--form-background);
		/* Not removed via appearance */
		margin: 0;

		font: inherit;
		color: currentColor;
		width: 1em;
		height: 1em;
		border: 0.1em solid currentColor;
		border-radius: 0.15em;
		transform: translateY(-0.075em);

		display: grid;
		place-content: center;
		cursor: pointer;
	}

	input[type="checkbox"]::before {
		content: "";
		width: 0.65em;
		height: 0.65em;
		clip-path: polygon(14% 44%, 0 65%, 50% 100%, 100% 16%, 80% 0%, 43% 62%);
		transform: scale(0);

		box-shadow: inset 1em 1em var(--form-control-color);
		background-color: $yellow;
	}

	input[type="checkbox"]:checked::before {
		transform: scale(1);
	}
	input[type="checkbox"]:checked + .label {
		color: $yellow;
	}
}

.tag-checkbox {
	label {
    color: $grey;
    font-weight: normal;
    background-color: $white;
    border: 1px solid $grey;
    padding-right: 1em;
    padding-top: 0.5em;
    padding-bottom: 0.5em;
    padding-left: 0.6em;
    &:hover {
      color: $grey;
      background-color: $lightergrey;
    }
	}
	input[type="checkbox"]::before {
		background-color: $grey;
	}
	input[type="checkbox"]:checked + .label {
		color: $darkgrey;
	}
}

a {
  color: $grey;
  &:hover {
    color: $purple;
  }
  &.active {
    font-weight: bold;
    color: #ef674b;
  }
}


</style>

<script>

export default {
  name: 'App',
  data () {
    return {
      loggedUser: 'Anonymous',
    }
  },
  computed: {
    loggedIn () {
      return this.$store.state.loggedIn;
    }
  },
  methods: {
    async updateUser () {
      if(this.loggedIn) {
        const data = await this.api({ method: 'get', url: `dj-rest-auth/user/` });
        this.loggedUser = data.username;
      }
    }
  },
  beforeCreate() {
    this.$store.commit('initStore');
  },
  watch: {
    loggedIn (newLoggedIn, oldLoggedIn) {
      this.updateUser();
    }
  },
  mounted () {
    this.updateUser();
  }
}
</script>
