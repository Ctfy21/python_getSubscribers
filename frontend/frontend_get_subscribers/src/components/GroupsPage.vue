<script>
export default {
    data(){
        return{
            groupsArray: ["https://test.com", "https://test.com", "https://test.com", "https://test.com"],
            url: ""
        }
    },
    methods: {
        addGroup() {
            this.groupsArray.push(this.url)
            this.url = ""
        }
    }
}

</script>

<template>
  <body>
    <div class="row">
      <div class="col m-4">
        <ul class="list-group list-group-flush">
          <li class="list-group-item" v-for="group in groupsArray" v-bind:key="group">
            {{  group  }}
          </li>
        </ul>
      </div>
      <div class="col m-4">
        <form @submit.prevent="addGroup(e)">
            <input v-model="url" type="text" class="form-control" placeholder="URL" aria-label="url">
            <button class="btn btn-outline-secondary mt-4">Добавить</button>
        </form>
      </div>
    </div>
  </body>
</template>

<style>

</style>
