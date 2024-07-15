const { createApp } = Vue

const App = {
    data(){
        return{
            groupsArray: [],
            url: "",

            accountsArray: [],
            api_id: "",
            api_hash: "",
            phone_number: "",
            password: "",
            result_send_chat: "",
            code_flag: false,
            telegram_code: ""

        }
    },
    methods: {
        async addGroup() {
            let new_group = {
                url: this.url
            }

            let json = JSON.stringify(new_group)

            await fetch('http://localhost:5000/add_group', {
                method: "POST",
                headers: {
                    'Content-Type': 'application/json;charset=utf-8'
                },
                body: json
            })

            window.location.reload(true)
        },
        async deleteGroup(group){
            let json = JSON.stringify(group)

            await fetch('http://localhost:5000/delete_group', {
                method: "DELETE",
                headers: {
                    'Content-Type': 'application/json;charset=utf-8'
                },
                body: json
            })

            window.location.reload(true)
        },

        async addAccount() {
            let new_account = {
                api_id: this.api_id,
                api_hash: this.api_hash,
                phone_number: this.phone_number,
                password: this.password,
                result_send_chat: this.result_send_chat
            }

            let json = JSON.stringify(new_account)
            await fetch('http://localhost:5000/add_account', {
                method: "POST",
                headers: {
                    'Content-Type': 'application/json;charset=utf-8'
                },
                body: json
            })

            this.code_flag = true

        },
        
        async sendTelegramCode() {
            let new_code = {
                code: this.telegram_code,
            }

            let json = JSON.stringify(new_code)
            await fetch('http://localhost:5000/post_telegram_code', {
                method: "POST",
                headers: {
                    'Content-Type': 'application/json;charset=utf-8'
                },
                body: json
            })

            window.location.reload(true)
        },    

        async editAccount() {
            await fetch('http://localhost:5000/edit_account', {
                method: "POST",
                headers: {
                    'Content-Type': 'application/json;charset=utf-8'
                },
                body: []
            })

            window.location.reload(true)
        },   


    },
    created() {
        fetch('http://localhost:5000/get_groups')
              .then(response => response.json())
              .then(data => (this.groupsArray = data))

        fetch('http://localhost:5000/get_account')
              .then(response => response.json())
              .then(data => (this.accountsArray = data))        
    },
    delimiters: ['{', '}']
}



createApp(App).mount('#app')

