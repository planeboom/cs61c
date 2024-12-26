$(document).ready(function () {
    $('#submit_button').on('click', function () {
        //1.登录操作
        let email = $('#email').val();
        let password = $('#password').val();
        let form_data = localStorage.getItem('form_data');
        if (form_data) {
            let data = JSON.parse(form_data);
            let flag_for_username = false;
            let flag_for_password = false;
            for (let i = 0; i < data.length; i++) {
                if (data[i].email == email && data[i].password == password) {
                    localStorage.setItem('cur_user', JSON.stringify([data[i]]));
                    flag_for_password = true;
                    flag_for_username = true;
                    break;
                } else if (data[i].email == email) {
                    flag_for_username = true;
                }
            }
            if (flag_for_password && flag_for_username) {
                alert("Log in successfully! Click 'My Self-learning' to return home page.");
            } else if (flag_for_username && !flag_for_password) {
                alert("Wrong password!");
            } else if (!flag_for_username) {
                alert('Account does not exist!');
            }
        } else {
            alert('Do not exist any acount!')
        }

    });
});