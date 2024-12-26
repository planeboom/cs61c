$(document).ready(function () {
    const $todosContainer = $('#todos-container');
    const payButton = $('#payButton');
    const username = $('#username').val(); // 从隐藏字段获取当前的 username
    // const paymentModal = new bootstrap.Modal($('#paymentModal')); // 支付 Modal
    // const loginModal = new bootstrap.Modal($('#loginModal')); // 登录提示 Modal
    //update current URL
    function updateURLParams(sortBy, page_num, city, cur_class, search, searchinfo) {
        const newURL = `${window.location.pathname}?sort_by=${sortBy}&page_num=${page_num}&city=${city}&cur_class=${cur_class}&searchinfo=${searchinfo}&search=${search}`;
        history.pushState(null, '', newURL);
    }


    // change page (complete/all/incomplete)
    $('.page').click(function () {
        const urlParams = new URLSearchParams(window.location.search);
        let curPage = $(this).data('id');
        let batch = urlParams.get('select') || 8;
        let page_num = 1;
        let sortBy = urlParams.get('sort_by') || 'date';
        updateURLParams(sortBy, curPage, batch, page_num);
        //give request through ajax
        $.ajax({
            url: '/page_change/' + curPage,
            type: "GET",
            data: {
                sort_by: sortBy,
                cur_page: curPage,
                select: batch,
                page_num: page_num
            },
            success: function (response) {
                // replace container
                $('#todos-container').html($(response).find('#todos-container').html());
            }
        });
    });
    const cookiesAccepted = localStorage.getItem("cookies_accepted");
    console.log(cookiesAccepted);
    if (!cookiesAccepted) {
    // 如果没有同意记录，显示 Cookie 警告
        $('.cookie-banner').show();
  }else{

        $('.cookie-banner').hide();

    }

     $('.order_submit').click(function () {
         console.log("here click");
        const pageData = $('.page_data');
        const userId = pageData.data('user-id');
        const concertId = pageData.data('concert-id');
        const day=$('.day-select').val();
         const price=$('.price-select').val();
         const quantity=$('.quantity-select').val();
        //give request through ajax
        $.ajax({
            url: '/order_submit' ,
            type: "POST",
            data: {
                user_id:userId,
                concert_id:concertId,
                day:day,
                price:price,
                quantity:quantity
            },
            success: function (response) {
            }
        });
    });

    $('.cbutton').click(function () {
        localStorage.setItem("cookies_accepted", "true");
      $('.cookie-banner').hide();
    });
    // reload current page
    $('.sort_link').click(function () {
        const urlParams = new URLSearchParams(window.location.search);
        let cur_class = urlParams.get('cur_class') || 'all';
        let city = urlParams.get('city') || 'all';
        let search = urlParams.get('search') || '0';
        let searchinfo = urlParams.get('searchinfo') || '';
        console.log(searchinfo);
        let page_num = 1;
        const sortBy = $(this).data('sort-by');
        const url = `/sort/${sortBy}`;
        $('.nav-link').removeClass('active');
        $(this).addClass('active');
        updateURLParams(sortBy, page_num, city, cur_class, search, searchinfo);

// through ajax send request
        $.ajax({
            url: url,
            type: "GET",
            data: {
                sort_by: sortBy,
                page_num: page_num,
                cur_class: cur_class,
                city: city,
                search: search,
                searchinfo: searchinfo,
            },
            success: function (response) {
                // 替换 todos 列表部分
                $('#todos-container').html($(response).find('#todos-container').html());
            }
        });
    });
    // change number of item per page
    $('#batch_select').change(function () {
        const urlParams = new URLSearchParams(window.location.search);
        let page_num = 1;
        let sortBy = urlParams.get('sort_by') || 'date';
        let curPage = urlParams.get('cur_page') || 'all';
        var batch = $(this).val();
        updateURLParams(sortBy, curPage, batch, page_num);

        if (batch) {

            $.ajax({
                url: '/batch_change/' + batch,
                type: 'GET',
                data: {
                    sort_by: sortBy,
                    cur_page: curPage,
                    select: batch,
                    page_num: page_num
                },
                success: function (response) {
                    $('#todos-container').html($(response).find('#todos-container').html());
                    $('#modal-container').html($(response).find('#modal-container').html());
                },
                error: function (xhr, status, error) {
                    console.error('Error:', error);
                }
            });
        }
    });
    payButton.on('click', function () {
        const price = parseFloat($('.price-select').val()) || 0; // 当前票价
        const quantity = parseInt($('.quantity-select').val()) || 0; // 当前数量
        const day = parseInt($('.day-select').val()) || 0; // 当前数量
        console.log(price, quantity, day);
        console.log(username);
        let a = price && quantity && day;
        console.log(a);
        if (a === 0) {
            $('#infoModal').show();
        } else if (username === 'None') {
            // 如果 username 不为空，显示支付 Modal
            $('#loginModal').show();
        } else {
            // 如果 username 为空，显示提示登录 Modal
            $('#paymentModal').show();
        }
    });
    $('#infoModal .close').on('click', function () {
        $('#infoModal').hide(); // 隐藏模态框
    });
    $('#loginModal .close').on('click', function () {
        $('#loginModal').hide(); // 隐藏模态框
    });
    $('#paymentModal .close').on('click', function () {
        $('#paymentModal').hide(); // 隐藏模态框
    });
    $('.price-select, .quantity-select').on('change', function () {
        // 获取当前选中的票价和数量
        const price = parseFloat($('.price-select').val()) || 0; // 当前票价
        const quantity = parseInt($('.quantity-select').val()) || 0; // 当前数量
        const total = price * quantity; // 计算总价

        // 更新总价显示
        $('.totol__price').text(`￥${total.toFixed(2)}`);
    });
// 事件委托：处理 class-choice 点击事件
    $(document).on('click', '.class-choice', function () {
        console.log("here");
        const urlParams = new URLSearchParams(window.location.search);
        let city = urlParams.get('city') || 'all';
        let page_num = 1;
        let sort_by = urlParams.get('sort_by') || 'name';
        const cur_class = $(this).data('class');
        let search = urlParams.get('search') || '0';
        let searchinfo = urlParams.get('searchinfo') || '';

        // 更新活动样式
        $('.class-choice').removeClass('factor-content-item-active');
        $(this).addClass('factor-content-item-active');

        // 更新 URL 参数
        updateURLParams(sort_by, page_num, city, cur_class, search, searchinfo);

        // 通过 Ajax 发送请求
        $.ajax({
            url: '/choose_class/' + cur_class,
            type: "GET",
            data: {
                sort_by: sort_by,
                page_num: page_num,
                cur_class: cur_class,
                city: city,
                search: search,
                searchinfo: searchinfo
            },
            success: function (response) {
                // 替换 todos 容器内容
                $('#todos-container').html($(response).find('#todos-container').html());
            }
        });
    });

// 事件委托：处理 city-choice 点击事件
    $(document).on('click', '.city-choice', function () {
        console.log("here");
        const urlParams = new URLSearchParams(window.location.search);
        let cur_class = urlParams.get('cur_class') || 'all';
        let page_num = 1;
        let sort_by = urlParams.get('sort_by') || 'name';
        const city = $(this).data('city');
        let search = urlParams.get('search') || '0';
        let searchinfo = urlParams.get('searchinfo') || '';

        // 更新活动样式
        $('.city-choice').removeClass('factor-content-item-active');
        $(this).addClass('factor-content-item-active');

        // 更新 URL 参数
        updateURLParams(sort_by, page_num, city, cur_class, search, searchinfo);

        // 通过 Ajax 发送请求
        $.ajax({
            url: '/city/' + city,
            type: "GET",
            data: {
                sort_by: sort_by,
                page_num: page_num,
                cur_class: cur_class,
                city: city,
                search: search,
                searchinfo: searchinfo
            },
            success: function (response) {
                // 替换 todos 容器内容
                $('#todos-container').html($(response).find('#todos-container').html());
            }
        });
    });
// delete one item


    $('.searchbutton').click(function () {
        const urlParams = new URLSearchParams(window.location.search);
        let cur_class = urlParams.get('cur_class') || 'all';
        let page_num = 1;
        let sort_by = urlParams.get('sort_by') || 'name';
        let city = urlParams.get('city') || 'all';
        let search = 1;
        const searchinfo = $('#searchinfo').val();
        const newURL = `/class?sort_by=${sort_by}&page_num=${page_num}&city=${city}&cur_class=${cur_class}&searchinfo=${searchinfo}&search=${search}`;
        history.pushState(null,'',newURL);
        // 通过 Ajax 发送请求
        $.ajax({
            url: '/search/' + searchinfo,
            type: "GET",
            data: {
                sort_by: sort_by,
                page_num: page_num,
                cur_class: cur_class,
                city: city,
                search: search,
                searchinfo: searchinfo
            },
            success: function (response) {
                // 替换 todos 容器内容
                console.log(response);
                $('body').html($(response).find('body').html());
                location.reload();
            }
        });
    });
    $todosContainer.on('click', '.delete-btn', function () {
        const todoId = $(this).data('id');  // get todo_id
        const urlParams = new URLSearchParams(window.location.search);
        let sortBy = urlParams.get('sort_by') || 'date';
        let page_num = urlParams.get('page_num') || 1;
        let curPage = urlParams.get('cur_page') || 'all';
        let batch = urlParams.get('select') || 8;
        updateURLParams(sortBy, curPage, batch, page_num);


        $.ajax({
            url: '/delete_todo/' + todoId,
            type: 'GET',
            data: {
                sort_by: sortBy,
                cur_page: curPage,
                select: batch,
                page_num: page_num
            },
            success: function (response) {

                $(`#modal_delete${todoId}`).modal('hide');
                $('#todos-container').html($(response).find('#todos-container').html());
                $('#modal-container').html($(response).find('#modal-container').html());
            },
            error: function (xhr, status, error) {
                console.error('error', error);
            }
        });
    });
    // edit one item
    // $(document).on('submit', '.editform', function (e) {
    //     e.preventdefault();
    //     const form = $(this);
    //     const todoid = form.data('id');
    //     $.ajax({
    //         url: '/edit/' + todoid,
    //         type: 'post',
    //         data: {
    //             ...form.serialize(),
    //         },
    //
    //         success: function (response) {
    //
    //             $('#modal_edit' + todoid).modal('hide');
    //
    //             $('#todos-container').html($(response).find('#todos-container').html());
    //             $('#modal-container').html($(response).find('#modal-container').html());
    //
    //
    //         },
    //         error: function (xhr, status, error) {
    //             console.error('error', error);
    //         }
    //     });
    // });
    // submit form for assessment
    $(document).on('submit', '.addform', function (e) {
        e.preventdefault();
        const form = $(this);
        $.ajax({
            url: '/submit_form/',
            type: 'POST',
            data: form.serialize(),
            success: function (response) {
                $('#modal_add').modal('hide');
                $('#todos-container').html($(response).find('#todos-container').html());
                $('#modal-container').html($(response).find('#modal-container').html());
            },
            error: function (xhr, status, error) {
                console.error('error', error);
            }
        });
    });
    // change page_num
    $todosContainer.on('click', '.page-link', function () {
        const urlParams = new URLSearchParams(window.location.search);


        let cur_class = urlParams.get('cur_class') || 'all';
        let city = urlParams.get('city') || 'all';
        let sortBy = urlParams.get('sort_by') || 'name';
        var page_num = $(this).data('index');
          let search = urlParams.get('search') || '0';
        let searchinfo = urlParams.get('searchinfo') || '';
        updateURLParams(sortBy, page_num, city, cur_class,search,searchinfo);
        $.ajax({
            url: '/page_num/' + page_num,
            method: 'GET',
            data: {
                sort_by: sortBy,
                page_num: page_num,
                city: city,
                cur_class: cur_class
            },
            success: function (response) {
                $('#todos-container').html($(response).find('#todos-container').html());
                $('#modal-container').html($(response).find('#modal-container').html());
            }
        });
    });

});

