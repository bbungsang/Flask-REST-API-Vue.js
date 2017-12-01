var app = new Vue({
  el: '#app',
  data: {
    quiz_list: [],
    answer: ""
  },
  created() {
    axios.get('http://127.0.0.1:5000/api/quiz/1')
    .then(response => {
      this.quiz_list = response.data
    })
    .catch(e => {
      this.errors.push(e)
    });
  },
  methods: {
    sendToServer: function() {
      axios({
        method: 'post',
        url: 'http://127.0.0.1:5000/api/quiz/1',
        data: {
          "answer": this.answer
        }
      })
      .then(function (response) {
        console.log(response);
      })
      .catch(function (error) {
        console.log(error);
      })
    }
  }
});
