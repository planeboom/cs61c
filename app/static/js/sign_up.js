$(document).ready(function () {

  // 1. 点击地区选择按钮后切换按钮文本（用select也可以但是select不美观）
  $('.dropdown-item').on('click', function () {
    let newText = $(this).text();
    $('.dropdown-toggle').text(newText);
  });

  //2.本地储存form data
  $('#submit_button').on('click', function () {
    let first_name = $('#first_name').val();
    let last_name = $('#last_name').val();
    let email = $('#inputEmail').val();
    let password = $('#inputPassword').val();
    let university = $('#inputuniversity').val();
    let phone = $('#inputphone').val();
    let area = $('.dropdown-toggle').text();
    let username = $('#inputUser').val();
    let job = $('#inputState').val();
    let gender = $('#inputGender').val();
    let name = first_name + " " + last_name;
    let new_data = {
      name: name, email: email, password: password, university: university, phone: area + " " + phone, phonenumber: phone,
      username: username, job: job, gender: gender, area: area
    };
    let form_data = localStorage.getItem('form_data');
    if (form_data) {
      let data = JSON.parse(form_data);
      if (valid_check(data, new_data)) {
        data.push(new_data);
        localStorage.setItem('form_data', JSON.stringify(data));
        alert("Registration is successful! Click 'sign in' to log in");
      }
    } else {
      localStorage.setItem('form_data', JSON.stringify([new_data]));
      alert("Registration is successful! Click 'sign in' to log in");
    }


  })
  //3. 判断数据合法性
  function valid_check(form_data, new_data) {
    if (new_data.area == 'Area') {
      alert("Choose your area!");
      return false;
    }
    if (!(digit(new_data.phonenumber))) {
      alert('Invalid phone number!')
      return false;
    }
    if (new_data.gender == 'Choose...') {
      alert('Please enter your gender!')
      return false;
    }
    if (new_data.job == 'Choose...') {
      alert('Please enter your job!')
      return false;
    }
    for (let i = 0; i < form_data.length; i++) {
      if (new_data.username == form_data[i].username) {
        alert('This User name has been used!');
        return false;
      } else if (new_data.phone == form_data[i].phone) {
        alert('This Phone number has been used!');
        return false;
      } else if (new_data.email == form_data[i].email) {
        alert('This email has been used!');
        return false;
      }
    }
    return true;
  }
  function digit(str) {
    return str.split('').every(char => char >= '0' && char <= '9');
  }
});