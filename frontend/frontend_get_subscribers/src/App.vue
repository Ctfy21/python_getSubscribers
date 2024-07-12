<script>
import MainHeader from './components/MainHeader.vue'
import GroupsPage from './components/GroupsPage.vue';

export default {
  components: {
    MainHeader,
    GroupsPage
  }
}

</script>

<template>
  <MainHeader></MainHeader>
  <GroupsPage></GroupsPage>
</template>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}
</style>
