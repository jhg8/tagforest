<template>
  <div class="graph">

    <span v-for="tag in entryTagList" v-bind:key="tag.name" >
      <router-link :to="getTagFilterUrl(tag.name)" :class="{ active: filterTagMap[tag.name] }" >
        {{ tag.name }}
      </router-link> |
    </span>

    <h2>Entries</h2>

      <p>
        <a @click.prevent="selectEntryMode = !selectEntryMode" href="#" >Select</a>
        <span v-if="selectEntryMode" > |
          <a @click.prevent="deleteSelectedEntry" href="#" >Delete</a>
        </span>
      </p>

      <span v-for="entry in entrySet" v-bind:key="entry.id" >
        <selectable
          @toggle="selectEntryIdMap.set(entry.id, !selectEntryIdMap.get(entry.id))"
          :select="selectEntryMode"
          :isSelected="selectEntryIdMap.get(entry.id)"
          :to="'/entry/' + entry.id"
        >{{ entry.name }}</selectable>
      </span>

    <h2>Tags</h2>


      <p>
        <a @click.prevent="selectTagMode = !selectTagMode" href="#" >Select</a>
        <span v-if="selectTagMode" > |
          <a @click.prevent="deleteSelectedTag" href="#" >Delete</a>
        </span>
      </p>

      <span v-for="tag in tagList" v-bind:key="tag.id" >
        <selectable
          @toggle="selectTagIdMap[tag.id] = !selectTagIdMap[tag.id]"
          :select="selectTagMode"
          :isSelected="selectTagIdMap[tag.id]"
          :to="'/tag/' + tag.id"
        >{{ tag.name }}</selectable>
      </span>

    <entry-upsert @entry-upsert="reload(filterQuery)" />
    <tag-upsert @tag-upsert="reload(filterQuery)" />

  </div>
</template>

<script>
import EntryUpsert from '@/components/EntryUpsert.vue';
import TagUpsert from '@/components/TagUpsert.vue';
import Selectable from '@/components/Selectable.vue';

export default {
  name: 'Graph',
  data() {
    return {
      // Data from backend
      entrySet: null,
      entryTagList: null,
      tagList: null,
      // Select menus
      selectEntryMode: false,
      selectEntryIdMap: new Map(),
      selectTagMode: false,
      selectTagIdMap: new Map(),
      // Tag filtering
      filterTagMap: {},
      filterQuery: '',
    };
  },
  components: {
    EntryUpsert,
    TagUpsert,
    Selectable,
  },
  computed: {
    loggedIn() {
      return this.$store.state.loggedIn;
    },
  },
  methods: {
    getTagFilterUrl(tag) {
      let url = '';

      const filterTagList = [];
      Object.keys(this.filterTagMap).forEach((t) => {
        if (t === tag) {
          if (!this.filterTagMap[t]) filterTagList.push(t);
        } else if (this.filterTagMap[t]) {
          filterTagList.push(t);
        }
      });

      if (filterTagList.length > 0) {
        url += `#${filterTagList.join('^')}`;
      }
      return url;
    },
    async reload(filterQuery) {
      this.filterQuery = filterQuery ? filterQuery.slice(1) : '';
      const url = filterQuery ? `graph/?q=${this.filterQuery}` : 'graph/';

      // Get data from Backend
      const data = await this.api({ method: 'get', url });

      // Refresh select Entry ID Map
      function refreshMap(map, newIdList) {
        const oldIdList = Array.from(map.keys());
        const newIdMap = new Map();
        newIdList.forEach((id) => {
          map.set(id, map.get(id) || false);
          newIdMap.set(id, true);
        });
        oldIdList.forEach((id) => {
          if (!(newIdMap.get(id) || false)) map.delete(id);
        });
      }

      refreshMap(this.selectEntryIdMap, Array.from(data.entry_set, (entry) => entry.id));
      refreshMap(this.selectTagIdMap, Array.from(data.tag_list, (tag) => tag.id));

      // Rebuild filterTagMap
      this.filterTagMap = {};
      data.entry_tag_list.forEach((tag) => {
        this.filterTagMap[tag.name] = false;
      });
      if (this.filterQuery) {
        const regEx = /[()|]/;
        let querySupported = true;
        const queryTagList = this.filterQuery.split('^');
        for (let i = 0; i < queryTagList.length; i += 1) {
          if (queryTagList[i].match(regEx)) {
            querySupported = false;
            break;
          }
        }
        if (querySupported) {
          queryTagList.forEach((tag) => { this.filterTagMap[tag] = true; });
        }
      }

      // Refresh entry and tag list
      this.entrySet = data.entry_set;
      this.entryTagList = data.entry_tag_list;
      this.tagList = data.tag_list;
    },
    async deleteSelectedEntry() {
      const deleteIdList = [];
      for (const [id, value] of this.selectEntryIdMap) {
        if (value) {
          await this.api({ method: 'delete', url: `entries/${id}/` });
          deleteIdList.push(id);
        }
      }
      for (let i = 0; i < deleteIdList.length; i += 1) {
        this.selectEntryIdMap.delete(deleteIdList[i]);
      }
      this.reload(this.filterQuery);
    },
    deleteSelectedTag() {
      //Object.keys(this.selectTagIdMap).forEach((id) => {
      //  if (this.selectTagIdMap[id]) {
      //    this.api({ method: 'delete', url: `tags/${id}/` });
      //    delete this.selectTagIdMap[id];
      //  }
      //});
      //this.reload(this.filterQuery);
    },
  },
  mounted() {
    this.reload(this.$route.hash);
  },
};
</script>
