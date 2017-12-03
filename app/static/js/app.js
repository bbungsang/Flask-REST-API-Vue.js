var count = 1;
if (localStorage.getItem('count')) {
  count = localStorage.getItem('count');
}
var app = new Vue({
  el: '#app',
  data: {
    quiz_list: [],
    answer: "",
    result: "",
    click: 0,
  },
  created() {
    axios.get('http://127.0.0.1:5000/api/solve/' + count)
    .then(response => {
      this.quiz_list = response.data;
    })
    .catch(e => {
      this.errors.push(e)
    });
  },
  methods: {
    showHint: function() {
      this.click++;
      var hint = document.getElementsByClassName("hint");
      if(this.click % 2 != 0) {
        var ct = document.getElementById("Q");
        ct.innerHTML = this.quiz_list.hint;
        hint[0].innerText = "문제 보기";
      } else {
        history.go(-1);
      }
    },
    sendToServer: function() {
      axios({
        method: 'post',
        url: 'http://127.0.0.1:5000/api/solve/' + count,
        data: {
          "answer": this.answer
        }
      })
      .then(response => {
        this.result = response.data;
      })
      .catch(e => {
        this.errors.push(e)
      });
    },
    prevQ: function () {
      count--;
      if(count == 0) {
        count = 1;
        alert("첫 번째 문제입니다.");
      }
      localStorage.setItem('count', count)
      axios.get('http://127.0.0.1:5000/api/solve/' + count)
        .then(response => {
          this.quiz_list = response.data;
        })
        .catch(e => {
          this.errors.push(e)
        });
      history.go(0);
    },
    nextQ: function () {
      count++;
      if(count > this.quiz_list.last_q) {
        count = this.quiz_list.last_q;
        alert("마지막 문제입니다.");
      }
      localStorage.setItem('count', count)
      axios.get('http://127.0.0.1:5000/api/solve/' + count)
        .then(response => {
          this.quiz_list = response.data;
        })
        .catch(e => {
          this.errors.push(e)
        });
      history.go(0);
    }
  }
});
