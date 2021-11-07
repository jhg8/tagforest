<template>

    <span v-if="select" >
      <a @click.prevent="toggle"
         :class="{ active: isSelected }"
         href="#" >
        <slot></slot>
      </a> |
    </span>
    <span v-else >
      <router-link :to="to" >
        <slot></slot>
      </router-link> |
    </span>

</template>

<script>

export default {
  name: 'Selectable',
  emits: ['toggle'],
  props: {
    select: Boolean,
    isSelected: Boolean,
    to: String,
  },
  methods: {
    toggle() {
      this.$emit('toggle');
    },
  },
};
</script>
