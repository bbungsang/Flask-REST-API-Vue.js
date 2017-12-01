var app = new Vue({
  el: '#app',
  data: {
    quiz_list: []
  },
  created() {
    axios.get('http://127.0.0.1:5000/api/quiz')
    .then(response => {
      this.quiz_list = response.data
    })
    .catch(e => {
      this.errors.push(e)
    })
  }
});
