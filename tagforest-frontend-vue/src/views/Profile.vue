<template>
  <section class="profile" ><div class="container" >
    <h1>{{ loggedUser }}</h1>
  </div></section>

  <section class="control-buttons" ><div class="container" >

    <button @click="showExportPopup = true" >
    <font-awesome-icon icon="fa-solid fa-download" /> Export
    </button>

    <button @click="showImportPopup = true" >
    <font-awesome-icon icon="fa-solid fa-upload" /> Import
    </button>

  </div></section>

  <section v-if="showExportPopup" class="popupExport"><div class="container" >
    <form class="textForm">
      <span class="textarea" ><textarea type="multiarea" v-model="exportValue" placeholder="Export" >
      </textarea></span>
      <button @click="showExportPopup = false" >Exit</button>
    </form>
  </div></section>

  <section v-if="showImportPopup" class="popupExport"><div class="container" >
    <form class="textForm" @submit.prevent="importData(); $emit('submit')" action="#" >
      <span class="textarea" ><textarea type="multiarea" v-model="importValue" placeholder="Import" >
      </textarea></span>
      <input type="submit" />
      <button @click="showImportPopup = false" >Cancel</button>
    </form>
  </div></section>

  <section class="profile" ><div class="container" >
    <p>
      <logout/>
    </p>
  </div></section>
</template>

<script>

import Logout from '@/components/Logout.vue'

export default {
  name: 'Profile',
  emits: ['import', 'cancel', 'submit'],
  components: {
    Logout
  },
  data () {
    return {
      loggedUser: 'Anonymous',
      importValue: '',
      exportValue: '',
      showExportPopup: false,
      showImportPopup: false
    }
  },
  methods: {
    async getUser () {
      const data = await this.api({ method: 'get', url: `dj-rest-auth/user/` });
      this.loggedUser = data.username;
    },
    async importData () {
      const data = {
        import_value: this.importValue
      };
      await this.api({ method: 'post', url: `import/`, data: data});
      this.$emit('import');
      this.$router.push({ path: '/'});
    },
    async getExportValue () {
      const data = await this.api({ method: 'get', url: `export/` });
      this.exportValue = JSON.stringify(data.export_value);
    }
  },
  mounted () {
    this.getUser();
    this.getExportValue();
  },
}
</script>
