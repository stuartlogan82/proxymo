const app = new Vue({
    el: '#main',
    data: {
        sessionName: '',
        sessionLength: '',
        restaurant: '',
        customer: '',
        proxy_num: '',
        proxyEstablished: false,
        message: 'Proxymo not yet configured!',
        isError: false,
        isLoading: false,
        timer: null

    },
    methods: {
        createSession: function () {
            
            vm = this;
            vm.message = "Establishing contact with Proxymo...";
            vm.isLoading = true;
            const payload = {
                sessionName: this.sessionName,
                sessionLength: this.sessionLength,
                restaurant: this.restaurant,
                customer: this.customer
            }
            console.log(payload)
            axios.post('/session/create', payload)
                .then(function (response) {
                    console.log(response.data);
                    const sessionSid = response.data.sessionSid;
                    const proxy1 = response.data.proxy1;
                    const proxy2 = response.data.proxy2;
                    vm.isLoading = false;
                    vm.proxyEstablished = true;
                    vm.message = "Use " + proxy1 + " to communicate! Session SID: " + sessionSid;
                     console.log(vm.sessionLength)
                     timeLeft = parseInt(vm.sessionLength);
                     console.log(timeLeft)
                     console.log(typeof (timeLeft))
                     timeKeeper = setInterval(function () {
                         timeLeft--;
                         console.log(timeLeft)
                         vm.timer = timeLeft.toString();
                         if (timeLeft <= 0) {
                             clearInterval(timeKeeper);
                             vm.message = "Proxymo Session Expired!"
                         }
                     }, 1000)
                })
                .catch(function (error) {
                    vm.isLoading = false;
                    vm.isError = true;
                    console.log(error)
                    vm.message = error.response.data[2];
                    console.log(error.response.data[2]);
                });
        
        },
        reset: function() {
            vm = this;
            Object.assign(vm.$data, vm.$options.data.call(vm))
        }
    }
});
Vue.config.devtools = true