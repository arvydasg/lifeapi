// document.addEventListener('DOMContentLoaded', function() {
//     document.body.style.backgroundColor = 'red';
// });

var answerFields = document.querySelectorAll('.answer-field');
answerFields.forEach(function(field) {
  var answer = field.textContent.trim();
  if (answer === 'YES') {
    field.style.backgroundColor = 'green';
    field.style.color = 'white';
  } else if (answer === 'NO') {
    field.style.backgroundColor = 'red';
    field.style.color = 'white';
  }
});