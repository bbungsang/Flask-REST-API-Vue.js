var count = 1;
if (localStorage.getItem('count')) {
  count = localStorage.getItem('count');
}
var app = new Vue({
  el: '#app',
  data: {
    quiz_list: [],
    answer: ""
  },
  created() {
    axios.get('http://127.0.0.1:5000/api/quiz/' + count)
    .then(response => {
      this.quiz_list = response.data;
    })
    .catch(e => {
      this.errors.push(e)
    });
  },
  methods: {
    showHint: function() {
      var ct = document.getElementById("Q");
      ct.innerHTML = this.quiz_list.hint;
    },
    sendToServer: function() {
      axios({
        method: 'post',
        url: 'http://127.0.0.1:5000/api/quiz/' + count,
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
    },
    prevQ: function () {
      count--;
      if(count == 0) {
        count = 1;
      }
      localStorage.setItem('count', count)
      axios.get('http://127.0.0.1:5000/api/quiz/' + count)
        .then(response => {
          this.quiz_list = response.data;
        })
        .catch(e => {
          this.errors.push(e)
        });
    },
    nextQ: function () {
      count++;
      if(count > this.quiz_list.last_q) {
        count = this.quiz_list.last_q;
      }
      localStorage.setItem('count', count)
      axios.get('http://127.0.0.1:5000/api/quiz/' + count)
        .then(response => {
          this.quiz_list = response.data;
        })
        .catch(e => {
          this.errors.push(e)
        });
    }
  }
});
