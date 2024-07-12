<script>
export default {
    data(){
        return{
            accountsArray: ["+79153374219", "+79153374219", "+79153374219", "+79153374219"],
            url: ""
        }
    },
    methods: {
        addAccount() {
            this.accountsArray.push(this.url)
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
          <li class="list-group-item" v-for="account in accountsArray" v-bind:key="account">
            {{  account  }}
          </li>
        </ul>
      </div>
      <div class="col m-4">
        <form @submit.prevent="addAccount(e)">
            <input v-model="url" type="text" class="form-control" placeholder="URL" aria-label="url">
            <button class="btn btn-outline-secondary mt-4">Добавить</button>
        </form>
      </div>
    </div>
  </body>
</template>

<style>

</style>
