function checkPageName() {
    return $('section.page').attr('id');
}

function objectConvertArray(obj) {
    if(typeof obj !== 'object') return obj
    let data = [];
    for (const i in obj) {
        data.push(obj[i])
    }
    return data
}

$(document).ready(function () {
    switch (checkPageName()) {
        case 'Login':
            loginPageEvent();
            break;

        case 'Coform':
            coformPageEvent();
        
        case 'Search':
            searchPageEvent();
            break;
        
        case 'Cashpymt':
            cashpymtPageEvent();
            break;

        default:
            break;
    }
    
    let dateClass = '.datepicker';
    if (checkDateTypeIsNotWorking(dateClass)) {
        updateStyleForIosSafariDatePicker(dateClass);
    }
})

function loginPageEvent() {
    const $login = $('.login');
    $login.find('input[type="text"]').attr('placeholder','請輸入帳號');
    $login.find('input[type="password"]').attr('placeholder','請輸入密碼');
}

function getStoreListHtml($select) {
    let html = `
        <option data-id="4" data-name="西華店" value="CG">CG / 西華店</option>
        <option data-id="5" data-name="復北店" value="CL">CL / 復北店</option>
        <option data-id="7" data-name="南西店" value="CB">CB / 南西店</option>
        <option data-id="8" data-name="忠孝店" value="CD">CD / 忠孝店</option>
        <option data-id="9" data-name="頂好店" value="CH">CH / 頂好店</option>
        <option data-id="10" data-name="仁愛店" value="CF">CF / 仁愛店</option>
        <option data-id="11" data-name="站前店" value="CE">CE / 站前店</option>
        <option data-id="12" data-name="公館店" value="CK">CK / 公館店</option>
        <option data-id="13" data-name="永和店" value="BA">BA / 永和店</option>
        <option data-id="14" data-name="新莊店" value="BB">BB / 新莊店</option>
        <option data-id="15" data-name="樹林店" value="BC">BC / 樹林店</option>
        <option data-id="16" data-name="光復店" value="FA">FA / 光復店</option>
        <option data-id="17" data-name="忠明店" value="ID">ID / 忠明店</option>
        <option data-id="18" data-name="文心店" value="IE">IE / 文心店</option>
        <option data-id="19" data-name="東寧店" value="PB">PB / 東寧店</option>
        <option data-id="20" data-name="崇學店" value="PC">PC / 崇學店</option>
        <option data-id="21" data-name="永康店" value="OA">OA / 永康店</option>
        <option data-id="22" data-name="三多店" value="RA">RA / 三多店</option>
        <option data-id="23" data-name="南京店" value="CA">CA / 南京店</option>`
    $select.find('.block_form_item_select.storeList').html(html);
}

function getTodayToInput($input) {
    let today = new Date();
    $input.val(`${today.getFullYear()}-${today.getMonth()+1}-${today.getDate()}`);
}


const $alert = $('#alert');

function alertMsg(type='success', msg='已送出!', errorText) {
    $alert.find('.alertmain h3').text(msg);
    $alert.addClass(`show ${type}`);
    $alert.off('click');
    let time = 1500;

    if (type === 'load' || type === 'question') return

    $alert.find('.alertBg').on('click', (e)=>{
        removeAlertMsg()
    });

    if (errorText) {
        $alert.find('.errorBlock_btn').show()
        $alert.find('.errorBlock_text').text(errorText);
        alertErrorTextOnClick();
        return
    } 

    let timer = null 
    timer = setTimeout(()=>{
        removeAlertMsg()
        clearTimeout(timer);
    }, time);
}

function removeAlertMsg() {
    $('#alert').attr('class', '');
    $alert.find('.errorBlock_btn').hide();
    $alert.find('.errorBlock_text').hide();
}

function alertErrorTextOnClick() {
    $alert.find('.errorBlock_btn').off('click')
    $alert.find('.errorBlock_btn').on('click', function () {
        $alert.find('.errorBlock_text').slideToggle();
        clearTimeout(alertMsg.timer);
    })
}


const Coform = {};
const $coform = $('section#Coform');
const $coform_view = $coform.find('.coform_view');
const $coform_modify = $coform.find('.coform_modify');
const $coform_main = $coform.find('.coform_main');
const $coform_new = $coform.find('.coform_new');

function coformPageEvent() {
    getStoreListHtml($coform);
    const num = $coform_new.find('#coform_title').data('num');
    const $sigleNum = $coform_new.find('#SingleNumber');
    const $storeId = $coform_new.find('#UnitName');
    $sigleNum.val(`${$storeId.val()}-${num}`);
    getTodayToInput($coform_main.find('.form_today'));
    coformBtnEvent();
    coformMainSearchEvent();
    coformModifyFormSendEvent();
    coformStoreOnChange();
    coformInputDisplayEvent();
    changeCardNumberBlur();
    listCheckedEvent($coform_modify);
}

function newCoformInit() {
    $coform_new.find('input:not("#SingleNumber"):not(".button"):not(".radio-input")').val('');
    $coform_new.find('#sign_img').empty();
    $coform_new.find('#BankName').val('000');
}

function listCheckedEvent($block) {
    $block.find('.list').on('click', 'input[type="checkbox"]', function () {
        $(this).parents('.list_item').toggleClass('checked');

        const isChecked = $(this).is(':checked');
        $(this).parents('.list_item').find('input').prop('required', isChecked);
    })
} 

function getCoformList(formData) {
    getData({
        url: 'coform/searchopen',
        data: formData,
        success(r) {
            console.log(r);
            if (r.data === undefined) {
                alertMsg('wrong', '查無資料!');

                goBackCoformMain();
                return false
            }
            $coform_modify.find('.list').empty();
            $coform_modify.find('.num_singleNumber').text(r.mod_id);
            getCoformListHtml(r.data);
            $('.outerLoading').hide();
        }
    })
}

function getCoformListHtml(datas) {
    let html = '';
    for (const i in datas) {
        const data = datas[i];
        html += `
            <div class="list_item" data-id="${data.order_id}">
                <div class="list_item_title">
                    <span>${data.order_id}</span>
                    <input type="checkbox" name="title" data-id="${data.order_id}">
                </div>
                <div class="list_item_main">
                    <div class="main_data">
                        <div class="list_item_main_item">
                            <div class="item_title">客戶編號</div>
                            <div class="item_value">${data.cust_id}</div>
                        </div>
                        <div class="list_item_main_item">
                            <div class="item_title">客戶姓名</div>
                            <div class="item_value">${data.cust_name}</div>
                        </div>
                        <div class="list_item_main_item">
                            <div class="item_title">付款金額</div>
                            <div class="item_value">${data.amount}</div>
                        </div>
                        <div class="list_item_main_item">
                            <div class="item_title">原授權碼</div>
                            <div class="item_value">${data.auth_code}</div>
                        </div>
                    </div>
                    
                    <div class="main_inputs">
                        <div class="input_item">
                            <div class="item_title">新授權碼</div>
                            <input class="item_value auth_code_new" type="text" />
                        </div>
                        <div class="input_item">
                            <div class="item_title">取授權日</div>
                            <div class="item_picker">
                                <input class="item_value datepicker auth_date" type="date" />
                                <i class="far fa-calendar"></i>
                            </div>
                        </div>
                        <div class="input_item">
                            <div class="item_title">請款日</div>
                            <div class="item_picker">
                                <input class="item_value datepicker req_date" type="date" />
                                <i class="far fa-calendar"></i>
                            </div>
                        </div>
                    </div>
                </div>
            </div>`;
    }

    $coform_modify.find('.list').html(html);

    // for ios desktop safari , because date type is not working
    let dateClass = '.datepicker';
    if (checkDateTypeIsNotWorking(dateClass)) {
        $(dateClass).datepicker().datepicker('option','dateFormat', 'yy/mm/dd');
    }
}

function coformModifyFormSendEvent() {
    $coform_modify.find('#coform_modify_form').on('submit', function () {
        let checkedList = getCheckedList();
        console.log(checkedList);
        if (checkedList.length > 10) {
            alertMsg('wrong','單次修改不可超過10筆資料!');
            return false
        }
        if (checkedList.length === 0) {
            alertMsg('wrong','未選取資料 無法送出!');
            return false
        }
        const lenthIs6 = (order) => order.auth_code.length === 6;
        if (!(checkedList.every(lenthIs6))) {
            alertMsg('wrong','新授權碼填入長度有誤!');
            return false
        }
        
        getData({
            url: 'modify/coform',
            data: {
                "data": checkedList
            },
            success(r) {
                console.log(r)
                alertMsg('success', '修改成功!');
                
                $coform_modify.hide();
                $coform_main.show();
            }
        })
        return false
    })
}

function coformMainSearchEvent() {
    $coform_main.find('.block_form').on('submit', function () {
        $coform_modify.find('.list').empty();
        $coform_modify.show();
        $coform_main.hide();
        const $main_storeId = $coform_main.find('#store_id :selected');
        const req_date = [$coform_main.find('#req_date_start').val(), $coform_main.find('#req_date_end').val()]
        
        const formData = {
            store_id: $main_storeId.val()
        }
        const cust_id = $coform_main.find('#cust_id').val();
        if (cust_id !== '') formData.cust_id = cust_id;

        const isNotEmpty = (day) => day !== '';
        const payway = $coform_main.find('#payway :selected').val();
        if (payway !== 'pay_all') formData.payway = payway;
        if (payway !== 'pay_later' && req_date.every(isNotEmpty)) formData.req_date = req_date;

        console.log('search',formData);
        
        const store_name = $main_storeId.data('name');
        $coform_modify.find('.store_singleNumber').text(store_name);

        $('.outerLoading').show();
        getCoformList(formData);

        return false
    })
}

function coformBtnEvent() {
    $coform_main.on('click', '.button', function () {

        if ($(this).attr('id') === 'NewCoform') { 
            newCoformInit();
            $coform_new.show();
            $coform_main.hide();
        }
    })
    
    $coform_modify.find('.buttons').on('click', '.button', function () {
        if ($(this).attr('id') === 'Cancel') {
            $coform_modify.find('.list').empty();
            goBackCoformMain('init');
        }
    })

    $coform_new.find('.buttons').on('click', '.button', function (e) {
        const thisId = $(this).attr('id');
        const last3 = $coform_new.find('#Card_last3Text').val();
        const $paycode = $coform_new.find('#PayCodeText');
        if (thisId === 'Cancel') {
            goBackCoformMain('init');
        }
        if (thisId === 'ViewForm') {
            console.log('ViewForm');
            if($coform_new.find('#sign_img').html() === '') {
                alertMsg('wrong', '未簽名無法送出預覽!');
                return false
            }
            if(last3 !== '' && last3.length !== 3) {
                alertMsg('wrong', '卡片後三碼有誤!');
                return false
            }
            if($paycode.attr('required') === 'required' && $paycode.val().length !== 6) {
                alertMsg('wrong', '授權碼長度有誤!');
                return false
            }
            
            const cardTimeArr = $('.coform_new #CardTime').find('.cardtime_input');
            let month = $(cardTimeArr[0]).val();
            let year = $(cardTimeArr[1]).val();
            if(parseInt(month) > 12 || month.toString().length !== 2 || year.toString().length !== 2) {
                alertMsg('wrong', '卡片有效期限有誤!');
                return false
            }

            const data = getNewCoformData();
            const bank = $coform_new.find('#BankName :selected').text();
            viewCoform(data, bank);
            console.log('打包',data);            
        }
    })
    $coform_new.find('.block_form').submit(function () {
        $coform_view.show();
        $coform_new.hide();
        $('.page').scrollTop(0);
        return false
    })

    $coform_view.find('.buttons').on('click', '.button', function () {
        const thisId = $(this).attr('id');
        if(thisId === 'Btn_print') {
            window.print();
        }
        if(thisId === 'Btn_cancel') {
            $coform_view.hide();
            $coform_new.show();
            $('.page').scrollTop(0);
        }
        if(thisId === 'Btn_send') {
            getData({
                url: 'coform', 
                success(r) {
                    console.log('sendData', Coform.data);
                    console.log('success', r);
                    alertMsg();
                    goBackCoformMain('init');

                    setTimeout(()=>{
                        location.reload();
                    }, 500);
                },
                data: Coform.data
            })
        }
    })
}

function getCheckedList() {
    const lists = $coform_modify.find('.list_item');
    let today = new Date();
    let checkedList = lists.map((i) => {
        const $list = $(lists[i]);
        if($list.find('.list_item_title input').is(':checked')) {
            return {
                mod_id: $coform_modify.find('.num_singleNumber').text(),
                coform_id: $list.data('id'),
                auth_code: $list.find('.auth_code_new').val(), //新授權碼
                auth_date: $list.find('.auth_date').val(), //取授權日
                req_date: $list.find('.req_date').val(), //請款日
                mod_date: today.toISOString().substring(0, 10),
                mod_r_id: $('#navbar_link_userId').text(),
                bank_req_date: $list.find('.req_date').val()
            }
        }
    })
    return checkedList.get()
}


function goBackCoformMain(init) {
    console.log('coform main init');
    $coform_main.show();
    $coform_new.hide();
    $coform_view.hide();
    $coform_modify.hide();
    
    if (init) {
        $coform_main.find('#cust_id').val('');
        $coform_main.find('.datepicker').val('');
    }
}


function coformInputDisplayEvent() {
    const $payCodeItem = $coform_new.find('#PayCodeText').parents('.block_form_item');
    const $GetPayCodeDateItem = $coform_new.find('#GetPayCodeDate').parents('.block_form_item');
    const $PayDateItem = $coform_new.find('#PayDate').parents('.block_form_item');
    
    $coform_new.find('.block_form').on('click', 'input[type="radio"]', function () {       
        const payCodeChecked = isCheckedStyle($coform_new.find('#PayCode'));

        changeDisplay($payCodeItem, payCodeChecked)
        changeDisplay($GetPayCodeDateItem, payCodeChecked);
        changeDisplay($PayDateItem, payCodeChecked);
    })
}

function isCheckedStyle($item) {
    return $item.prop('checked') ? true : false;
}

function changeDisplay($item, state) {
    let visibilityText = state ? 'initial' : 'hidden';
    $item.css('visibility', visibilityText);
    $item.find('input').prop('required', state);
}

function coformStoreOnChange() {
    const num = $coform_new.find('#coform_title').data('num');
    const $sigleNum = $coform_new.find('#SingleNumber');
    const $storeId = $coform_new.find('#UnitName');
    $storeId.on('change', function () {
        $sigleNum.val(`${$storeId.val()}-${num}`);
    })
}

function getNewCoformData() {

    let card_num = '';
    const cardInputs = $('.coform_new #CardId').find('.card_input');
    for(let i = 0; i < cardInputs.length; i++) {
        card_num += $(cardInputs[i]).val();
    }

    let card_exp = '';
    const cardTimeArr = $('.coform_new #CardTime').find('.cardtime_input');
    card_exp = `${$(cardTimeArr[0]).val()}-20${$(cardTimeArr[1]).val()}`

    const last3Text = $coform_new.find('#Card_last3Text').val();
    const last3 = last3Text !== '' ? last3Text : null;
    const isPayCode = $coform_new.find('#PayCode').prop('checked');
    let auth_code = isPayCode ? $coform_new.find('#PayCodeText').val() : '';
    let auth_date = isPayCode ? $coform_new.find('#GetPayCodeDate').val() : '';
    let req_date = isPayCode ? $coform_new.find('#PayDate').val() : '';

    return {
        order_id: $coform_new.find('#SingleNumber').val(), //單號
        store_id: $coform_new.find('#UnitName :selected').val(), //分店代碼
        amount: $coform_new.find('#TotalAmount').val(), // 金額
        r_id: $('.navbar_link_user #navbar_link_userId').text(), //紀錄者工號
        r_name: $('.navbar_link_user #navbar_link_userName').text(), //紀錄者姓名
        auth_code, // 授權碼
        auth_date, // 授權日期
        req_date, // 請款日期
        card_holder: $coform_new.find('#CardUserName').val(), // 持卡人姓名
        cust_name: $coform_new.find('#ClientName').val(), // 客戶姓名
        cust_id: $coform_new.find('#ClientId').val(), // 會員ID
        card_num, // 卡號
        bank: $coform_new.find('#BankName').val(), // 銀行代號
        card_exp, // 卡片期限
        payway: $coform_new.find('#PayType input[name="payType"]:checked').val(), //付款方式
        last3, // 後三碼
        store_name: $coform_new.find('#UnitName :selected').data('name'), // 店家名稱
        signature: $coform_new.find('#image_data').attr('src'), // 簽名
    }
}



function viewCoform(data, bankName) {
    Coform.data = data;
    showDataInViewCoform(data);
    showCheckedInViewCoform(data);
    showStoreTitle(data.store_id, $coform_view);

    const authDate = data.auth_date;
    const reqDate = data.req_date
    let roc = '民國　　　　年　　　月　　　日'
    let auth = authDate !== '' ? changeCoformDate(authDate) : roc;
    let req = authDate !== '' ? changeCoformDate(reqDate) : roc;
    $coform_view.find('#View_auth_date').text(auth);
    $coform_view.find('#View_req_date').text(req);
    $coform_view.find('#View_card_exp').text(changeCoformDate(data.card_exp));
    $coform_view.find('#View_bankName').text(bankName);
    $coform_view.find('#View_card_num').text(formatCodeNum(data.card_num));
    $coform_view.find('#View_storeName').text(`${data.store_id} / ${data.store_name}`)
    $coform_view.find('#View_sign_img').html(`<img src="${data.signature}" alt="sign">`);
}

function changeCardNumberBlur() {
    const $last3 =$('#Card_last3Text');
    $coform_new.find('.card_input').on('keyup', function(e) {
        $(this).val($(this).val().replace(/[^0-9]/g, ''))
        if ($(this).val().length === 4) {
            $(this).next(':input').focus(); 
            if ($(this).data('index') === 3) $last3.focus();
        }
        if ($(this).attr('id') === 'Card_last3Text') {
            if ($(this).val().length === 3) $('#CardTime .card_input0').focus();
        }
    })
    $coform_new.find('#CardTime .cardtime_input').on('keyup', function(e) {
        if ($(this).val().length === 2) {
            if ($(this).data('index') === 1) {
                $('#TotalAmount').focus();
            } else {
                $(this).next(':input').focus(); 
            }
        }
    })
}


function formatCodeNum(data) {
    let card_num = [];
    for (let i = 0; i < data.length; i++) {
        let num = data[i];
        if(i !== 0 && (i+1) % 4 === 0 && i !== 15) num += '-';
        card_num.push(num);
    }
    return card_num.join('')
}

function changeCoformDate(date) {
    let day = date.split('-');
    if (date.length > 7) {
        return `民國 
        ${day[0]-1911} 年 
        ${day[1]} 月 
        ${day[2]} 日`
    }
    else {
        return ` 
        ${day[0]} 月 (西元) 
        ${day[1]} 年 
        `
    }
}

function showStoreTitle(id, $block) {
    console.log(id);
    const $detail = $block.find('.storeDetail');
    $block.find('.store2.title').hide();
    $detail.find('.store').hide();
    $block.find(`.store2.title.${id}`).show();
    $detail.find(`.store.${id}`).show()
}

function showDataInViewCoform(data) {
    const viewTexts = $coform_view.find('.viewText');
    for (let i = 0; i < viewTexts.length; i++) {
        const itemId = $(viewTexts[i]).attr('id');
        
        let id = itemId.slice(5,itemId.length);
        $(viewTexts[i]).text(data[id]);
    }
}

function showCheckedInViewCoform(data) {
    let payType = data.payway === 'payCode' ? 'PayCode' : 'LatePay';
    $(`#View_${payType}`).prop('checked',true);
}


function loadPrintCss() {

    let head = document.getElementsByTagName('HEAD').item(0);
    let style = document.createElement('link');

    style.href = document.body.clientWidth> 1200 ? '/static/css/print.css' : '/static/css/print_pad.css';
    
    style.media = 'print';
    style.rel = 'stylesheet';
    style.type = 'text/css';

    head.appendChild(style);
}

const Cashpymt = {};
const $cashpymt = $('#Cashpymt');
const $cashpymt_start = $cashpymt.find('.cashpymt_start');
const $cashpymt_getList = $cashpymt.find('.cashpymt_getList');
const $cashpymt_send = $cashpymt.find('.cashpymt_send');

function cashpymtPageEvent() {
    
    getStoreListHtml($cashpymt);
    const num = $cashpymt_start.find('#cashpymt_start_title').data('num');
    const store = $cashpymt_start.find('#store_id :selected').val();
    $cashpymt_start.find('#cashpymt_id').val(store+'-'+num);
    cashpymtOnChange($cashpymt_start);
    cashpymtStartSubmit($cashpymt_start);
    cashpymtGetListOnClick();
    cashpymtsendOnClick($cashpymt_start);
    listCheckedEvent($cashpymt);
}

function cashpymtStartSubmit($startBlock) {
    
    $startBlock.find('.block_form').on('submit', function () {
        const refund_ind = $startBlock.find('input[name*="cashType"]:checked').val() === 'remit' ? 0 : 1;
        const deposit_date = $startBlock.find('#deposit_date').val();

        $cashpymt_send.data('num', $startBlock.find('#cashpymt_id').val()); // 單號
        console.log('cashpymt submit',{
            store_id: $startBlock.find('#store_id').val(),
            pymt_date: [$startBlock.find('#src_dateFrom').val(), $startBlock.find('#src_dateTo').val()],
            refund_ind, 
        });
        $startBlock.hide();
        $cashpymt_getList.show();
        $cashpymt_getList.find('.outerLoading').show();

        getData({
            url: 'cashpymt',
            data: {
                store_id: $startBlock.find('#store_id').val(),
                store_name: $startBlock.find('#store_id :selected').data('name'),
                pymt_date: [$startBlock.find('#src_dateFrom').val(), $startBlock.find('#src_dateTo').val()],
                refund_ind, 
            },
            success(r) {
                console.log(r);
                if(Object.keys(r).length === 0) {
                    removeAlertMsg();
                    alertMsg('wrong', '查無資料!');

                    $startBlock.show();
                    $cashpymt_getList.hide();
                    return false
                }
                const data = objectConvertArray(r)
                cashpymtShowListHtml(data);
                $cashpymt_getList.find('.outerLoading').hide();
            },
            error() {
                $startBlock.show();
                $cashpymt_getList.hide();
            }
        })

        Cashpymt.deposit_date = deposit_date;
        return false
    })
}

function cashpymtShowListHtml(datas, type='get') {
    Cashpymt.allList = datas;
    const item = type === 'get' ? 'cashpymt_getList' : 'cashpymt_send';

    let html = '';
    for (let i = 0; i < datas.length; i++) {
        const data = datas[i]
        const refundText = data.refund_ind == 0 ? '匯款' : '退款';
        html += `
            <div class="list_item" data-id="${data.pymt_order_seq}">
                <div class="list_item_title">
                    <span class="singleNumber" id="pymt_order_seq">${data.pymt_order_seq}</span>
                    <input type="checkbox" name="title" class="pymt_order_id_checkbox" data-id="${data.pymt_order_seq}">
                </div>
                <div class="list_item_main">
                    <div class="main_row">
                        <div class="list_item_main_item">
                            <div class="item_title">分店名稱</div>
                            <div class="item_value store" id="store" >${data.store_id} / ${data.store_name}</div>
                        </div>
                        <div class="list_item_main_item">
                            <div class="item_title">客戶編號</div>
                            <div class="item_value" id="cust_id">${data.cust_id}</div>
                        </div>
                        <div class="list_item_main_item">
                            <div class="item_title">客戶姓名</div>
                            <div class="item_value" id="cust_name">${data.cust_name}</div>
                        </div>
                    </div>
                    
                    <div class="main_row">
                        <div class="list_item_main_item">
                            <div class="item_title">匯款或退款</div>
                            <div class="item_value identificationCode" id="refund_ind">${refundText}</div>
                        </div>
                        <div class="list_item_main_item">
                            <div class="item_title">付(退)款日期</div>
                            <div class="item_value cashTypeDate" id="data_src_date">${data.data_src_date}</div>
                        </div>
                        <div class="list_item_main_item">
                            <div class="item_title">付(退)款金額</div>
                            <div class="item_value cashTypeCash" id="pymt_amt">${data.pymt_amt}</div>
                        </div>
                        ${type === 'send' ? 
                            `<div class="list_item_main_item">
                                <div class="item_title">匯款日期</div>
                                <div class="item_value deposit_date" id="deposit_date">${Cashpymt.deposit_date}</div>
                            </div>` : ''
                        }
                    </div>
                </div>
            </div>`;        
    }
    $cashpymt.find(`.${item} .list`).html(html);
}



function cashpymtGetListOnClick() {
    // signNum
    $cashpymt_getList.on('click', '.button', function() {
        if ($(this).attr('id') === 'GetList_Cancel') {
            $cashpymt_getList.hide();
            $cashpymt_getList.find('.list').empty();
            $cashpymt_start.show();
            return
        }

        let checkedList = getCheckedIndex($cashpymt_getList, 'allList')
        console.log('checkedList', checkedList);
        if (checkedList.length === 0) {
            alertMsg('wrong','未選取資料!');
            return false
        }
        Cashpymt.retrieveList = checkedList;
        cashpymtShowListHtml(checkedList, 'send');

        $cashpymt_getList.hide();
        $cashpymt_send.show();
    })
}

function cashpymtsendOnClick($startBlock) {
    $cashpymt_send.on('click', '.button', function () {

        if($(this).attr('id') === 'Send_Cancel') {
            $cashpymt_send.hide();
            $cashpymt_getList.find('.list').empty();
            $startBlock.show();
            return 
        }

        let checkedList = getCheckedIndex($cashpymt_send, 'retrieveList');
        
        if (checkedList.length === 0) {
            alertMsg('wrong','未選取資料!');
            return false
        }
        console.log('cashpymtsend', {
            r_id: $('#navbar_link_userId').text(),
            r_name: $('#navbar_link_userName').text(),
            cashpymt_id: $cashpymt_send.find('#cashpymt_id').text(),
            data: checkedList.get()
        });
        alertMsg('load');
        getData({
            url: 'cashpymtsend',
            data: {
                deposit_date: Cashpymt.deposit_date,
                r_id: $('#navbar_link_userId').text(),
                r_name: $('#navbar_link_userName').text(),
                cashpymt_id: $cashpymt_send.find('#cashpymt_id').text(),
                data: checkedList.get()
            },
            success(r) {
                console.log(r);
                removeAlertMsg();
                alertMsg('success','已送出!');
                $cashpymt_getList.find('.list').empty();
                $cashpymt_send.hide();
                $startBlock.show();
                setTimeout(()=>{
                    location.reload();
                }, 500);
            }
        })
    })
}

function getCheckedIndex($outer, array) {
    const lists = $outer.find('.list_item');
    let checkedList = lists.map((i) => {
        const $list = $(lists[i]);
        if($list.find('.pymt_order_id_checkbox').is(':checked')) {
            return Cashpymt[array][i]
        }
    })
    return checkedList
}

function cashpymtOnChange($startBlock) {
    const num = $startBlock.find('#cashpymt_start_title').data('num');
    const $send_cashpymt_id = $('#Cashpymt').find('.cashpymt_send #cashpymt_id');
    const $start_cashpymt_id = $startBlock.find('#cashpymt_id');
    const $storeId = $startBlock.find('#store_id');
    const nowId = $storeId.val() + '-' + num;
    // 更新第一次單號
    $start_cashpymt_id.text(nowId);
    $send_cashpymt_id.text(nowId);

    $storeId.on('change', function () {

        const val = $(this).val()+ '-' + num;
        $start_cashpymt_id.val(val);
        $send_cashpymt_id.text(val);
    })
}


function checkDateTypeIsNotWorking(dateClass) {
    if ($(dateClass).length === 0) return false
    return document.querySelector(dateClass).type !== 'date'
}

function updateStyleForIosSafariDatePicker(dateClass) {
    // for ios desktop safari , because date type is not working

    let oCSS = document.createElement('link');
    oCSS.type='text/css'; oCSS.rel='stylesheet';
    oCSS.href='//ajax.googleapis.com/ajax/libs/jqueryui/1.12.1/themes/base/jquery-ui.css';
    oCSS.onload=function() {
        let oJS = document.createElement('script');
        oJS.type='text/javascript';
        oJS.src='//ajax.googleapis.com/ajax/libs/jqueryui/1.12.1/jquery-ui.min.js';
        oJS.onload=function() {
            $(dateClass).datepicker().datepicker('option','dateFormat', 'yy/mm/dd');
        }
        document.body.appendChild(oJS);
    }
    document.body.appendChild(oCSS);
}


const $search = $('#Search');
const $condition_block = $search.find('.condition_block');
const $search_main = $search.find('.search_main');
const $search_coform = $search.find('#search_coform');
const $search_cashpymt = $search.find('#search_cashpymt');
const $alertViewcoform = $('#alertViewcoform');


function searchPageEvent() {
    itemdisabledChange();
    getStoreListHtml($search);
    searchOnClick();
    searchEformOnClick();
    deleteCashpymt();
    searchPageCashpymtStatusOnChange();
    cashpymtToCsvEvent();
    searchPageViewCoform();
    searchPageViewCoformEvent();
}

function statusOptionOnChange() {
    $search_coform.find('.current_status').on('change', function () {
        const color = $(this).find('option:selected').attr('class');
        $(this).attr('class', color + ' current_status');
        $(this).parents('tr').attr('class', color);
    })
}

function itemdisabledChange() {
    $search.on('click', '.condition', function () {
        const checkedType = $(this).is(':checked') ? false : 'disabled';
        $(this).parents('.search_item').find('.checkedValueBox').attr('disabled',checkedType);
    })
}

function getSearchCondition() {
    const checkedList = $search_main.find('input.condition:checked');
    const conditions = {};
    checkedList.map((i,input)=>{
        const $val = $(input).parents('.search_item').find('.condition_value');
        const thisKey = $(input).data('name');
        if ($val.length > 1) {
            const items = $val;
            conditions[thisKey] = [$(items[0]).val(),$(items[1]).val()];
            return
        }
        if (thisKey === 'store_name') {
            conditions[thisKey] = $val.find(':selected').data('name');
            return
        }
        conditions[thisKey] = $val.val();
    })

    return conditions
}

function searchOnClick() {
    $search_main.on('submit', function () {
        const pageId = $('.pageNavBar_item.active').data('name');
        console.log(getSearchCondition());
        alertMsg('load');

        let url;
        const status = $search_main.find('#Cashpymt_status').val();
        url = status === '未送出' ? pageId : 'search/' + pageId;
        console.log('url',url);
        // wait api
        getData({
            url,
            data: getSearchCondition(),
            success(r) {
                if(Object.keys(r).length === 0) {
                    removeAlertMsg();
                    alertMsg('wrong', '查無資料!');
                    return false
                }
                
                removeAlertMsg();

                if (pageId === 'mailorder') {
                    console.log(r);
                    showCoformInTable(r);
                    statusOptionOnChange();
                    $condition_block.hide();
                    $search_coform.show();
                }
                if (pageId === 'cashpymt') {
                    console.log(r);
                    $search_cashpymt.data('type', status);
                    showCashpymtInTable(r, url);
                    $condition_block.hide();
                    $search_cashpymt.show();
                }
            }
        })

        return false
    })
}

function showCashpymtInTable(data, url) {
    let html = ''
    for (const i in data) {
        const order = data[i];
        if (url === 'cashpymt') {
            // 狀態為未送出
            html += `
            <tr>
                <td headers="operation">
                    <div>/</div>
                </td>
                <td headers="cashPymt_id">未匯款</td>
                <td headers="store_id">${order.store_id}</td>
                <td headers="store_name">${order.store_name}</td>
                <td headers="cust_id">${order.cust_id}</td>
                <td headers="cust_name">${order.cust_name}</td>
                <td headers="data_src_date">${order.data_src_date}</td>
                <td headers="pymt_order_id">${order.pymt_order_id}</td>
                <td headers="pymt_order_seq">${order.pymt_order_seq}</td>
                <td headers="pymt_amt">${order.pymt_amt}</td>
                <td headers="deposit_date">/</td>
                <td headers="r_id">/</td>
                <td headers="r_name">/</td>
                <td headers="etl_dttm">${order.etl_dttm}</td>
            </tr>`;
        } else {
            // 狀態為已送出
            html += `
            <tr>
                <td headers="operation">
                    <div class="del button" data-id="${order.cashpymt_id}">刪除</div>
                </td>
                <td headers="cashPymt_id">${order.cashpymt_id}</td>
                <td headers="store_id">${order.store_id}</td>
                <td headers="store_name">${order.store_name}</td>
                <td headers="cust_id">${order.cust_id}</td>
                <td headers="cust_name">${order.cust_name}</td>
                <td headers="data_src_date">${order.data_src_date}</td>
                <td headers="pymt_order_id">${order.pymt_order_id}</td>
                <td headers="pymt_order_seq">${order.pymt_order_seq}</td>
                <td headers="pymt_amt">${order.pymt_amt}</td>
                <td headers="deposit_date">${order.deposit_date}</td>
                <td headers="r_id">${order.r_id}</td>
                <td headers="r_name">${order.r_name}</td>
                <td headers="data_dttm">${order.data_dttm}</td>
            </tr>`;
        }
    }
    $search_cashpymt.find('tbody').html(html);  
}

function showCoformInTable(data) {
    let html = ''
    for (const i in data) {
        const order = data[i];
        html += `
            <tr class="${getSelectClass(order.status)}" data-sign="${order.signature}">
                <td headers="view"><button class="view btn">預覽</button></td>
                <td headers="status">
                    <div class="selectBox">
                        <select class="current_status ${getSelectClass(order.status)}" name="current_status">
                            <option class="blue" value="已請款" ${checkedState('已請款', order.status)}>已請款</option>
                            <option class="orange" value="未請款" ${checkedState('未請款', order.status)}>未請款</option> 
                            <option class="pink" value="作廢" ${checkedState('作廢', order.status)}>作廢</option>
                            <option class="yellow" value="退款" ${checkedState('退款', order.status)}>退款</option>
                        </select>
                    </div>
                </td>
                <td headers="order_id">${order.order_id}</td>
                <td headers="store_name">${order.store_name}</td>
                <td headers="r_id">${order.r_id}</td>
                <td headers="r_name">${order.r_name}</td>
                <td headers="auth_code" contenteditable="true">${order.auth_code}</td>
                <td headers="auth_date" contenteditable="true">${order.auth_date}</td>
                <td headers="req_date" contenteditable="true">${order.req_date}</td>
                <td headers="bank_req_date" contenteditable="true">${order.bank_req_date}</td>
                <td headers="card_holder">${order.card_holder}</td>
                <td headers="cust_name">${order.cust_name}</td>
                <td headers="cust_id">${order.cust_id}</td>
                <td headers="card_num">${order.card_num}</td>
                <td headers="last3">${order.last3}</td>
                <td headers="bank">${order.bank}</td>
                <td headers="card_exp">${order.card_exp}</td>
                <td headers="payway">${order.payway}</td>
                <td headers="amount">${order.amount}</td>
                <td headers="mod_date">${order.mod_date}</td>
                <td headers="mod_r_id">${order.mod_r_id}</td>
            </tr>`;
    }
    $search_coform.find('tbody').html(html);  
}

function getSelectClass(status) {
    if (status === '已請款') return 'blue'
    else if (status === '未請款') return 'orange'
    else if (status === '作廢') return 'pink'
    else if (status === '退款') return 'yellow'
    else return ''
}

function checkedState(text, status) {
    return status === text ? 'selected' : ''
}

function getCoformTableData() {
    const $tbody = $search_coform.find('tbody');
    const orders = $tbody.find('tr');
    const datas = [];
    orders.map((i, tr) => {
        const $tr = $(tr);
        datas.push({
            status: $tr.find('.current_status').val(),
            order_id: $tr.find('td[headers="order_id"]').text(),
            store_name: $tr.find('td[headers="store_name"]').text(),
            r_id: $tr.find('td[headers="r_id"]').text(),
            r_name: $tr.find('td[headers="r_name"]').text(),
            auth_code: $tr.find('td[headers="auth_code"]').text(),
            auth_date: $tr.find('td[headers="auth_date"]').text(),
            req_date: $tr.find('td[headers="req_date"]').text(),
            bank_req_date: $tr.find('td[headers="bank_req_date"]').text(),
            card_holder: $tr.find('td[headers="card_holder"]').text(),
            cust_name: $tr.find('td[headers="cust_name"]').text(),
            cust_id: $tr.find('td[headers="cust_id"]').text(),
            card_num: $tr.find('td[headers="card_num"]').text(),
            last3: $tr.find('td[headers="last3"]').text(),
            bank: $tr.find('td[headers="bank"]').text(),
            card_exp: $tr.find('td[headers="card_exp"]').text(),
            payway: $tr.find('td[headers="payway"]').text(),
            amount: $tr.find('td[headers="amount"]').text(),
            mod_date: $tr.find('td[headers="mod_date"]').text(),
            mod_r_id: $tr.find('td[headers="mod_r_id"]').text()
        })
    })
    return datas
}

function getCashpymtTableData() {
    const status = $search_cashpymt.data('type');
    const $tbody = $search_cashpymt.find('tbody');
    const orders = $tbody.find('tr');
    const datas = [];
    let dttm = status === '已送出' ? 'data_dttm' : 'etl_dttm'
    orders.map((i, tr) => {
        const $tr = $(tr);
        datas.push({
            cashPymt_id: $tr.find('td[headers="cashPymt_id"]').text(),
            store_id: $tr.find('td[headers="store_id"]').text(),
            store_name: $tr.find('td[headers="store_name"]').text(),
            cust_id: $tr.find('td[headers="cust_id"]').text(),
            cust_name: $tr.find('td[headers="cust_name"]').text(),
            data_src_date: $tr.find('td[headers="data_src_date"]').text(),
            pymt_order_id: $tr.find('td[headers="pymt_order_id"]').text(),
            pymt_order_seq: $tr.find('td[headers="pymt_order_seq"]').text(),
            pymt_amt: $tr.find('td[headers="pymt_amt"]').text(),
            deposit_date: $tr.find('td[headers="deposit_date"]').text(),
            r_id: $tr.find('td[headers="r_id"]').text(),
            r_name: $tr.find('td[headers="r_name"]').text()
        })
        let td_dttm = `td[headers=${dttm}]`;
        datas[i][dttm] = $tr.find(td_dttm).text();
    })
    return datas
}

function searchEformOnClick() {
    $search_coform.on('click', '.button', function () {
        alertMsg('load');
        if ($(this).attr('id') === 'Save') {
            const allData = getCoformTableData()
            console.log(allData);

            const lenthIs6 = (order) => order.auth_code.length === 6;
            if (!(allData.every(lenthIs6))) {
                removeAlertMsg();
                alertMsg('wrong','授權碼填入長度有誤!');
                return false
            }
            getData({
                url: 'search/mailorder/update',
                data: {
                    data: allData
                },
                success(r) {
                    console.log(r);
                    removeAlertMsg();
                    alertMsg('success','修改成功!');
                }
            })
        }
        if ($(this).attr('id') === 'Export') {

            downloadFile(getCoformTableData())
            getData({
                url: 'search/mailorder/update',
                data: {
                    data: getCoformTableData()
                },
                success(r) {
                    console.log(r);
                }
            })
        }
    })
}

function cashpymtToCsvEvent() {
    $search_cashpymt.find('#Export').click(function () {
        downloadFile(getCashpymtTableData())
    })
}

function downloadFile(data) {
    //藉型別陣列建構的 blob 來建立 URL
    let fileName = "coform.csv";
    let jsonData = JSON.stringify(data)
    let formatData = Papa.unparse(jsonData); // JSON to csv
    
    let blob = new Blob([formatData], {
        type: "application/octet-stream"
    });
    let href = URL.createObjectURL(blob);
    // 從 Blob 取出資料
    let link = document.createElement("a");
    document.body.appendChild(link);
    link.href = href;
    link.download = fileName;
    link.click();
    link.remove();
    URL.revokeObjectURL(link.href);

    removeAlertMsg();
  }
  

function deleteCashpymt() {
    $search_cashpymt.find('tbody').on('click','.button.del', function () {
        const $tr = $(this).parents('tr');
        alertMsg('question');
        alertQuestionOnclick($tr, $(this).data('id'))
    })
}

function alertQuestionOnclick($item, id) {
    $alert.find('.checkBtns').off('click');
    $alert.find('.checkBtns').on('click', '.button', function () {
        removeAlertMsg();

        if($(this).data('type')) {
            deleteCashpyData({
                id: id,
                success() {
                    $item.remove();
                }
            })
        }
    })
}

function searchPageCashpymtStatusOnChange() {
    const $send = $search_main.find('.sendCondition');
    const $notSend = $search_main.find('.notSendCondition');
    const $refund_ind = $notSend.find('.condition.refund_ind');
    $refund_ind.prop('checked', false);

    $search_main.find('#Cashpymt_status').on('change',function () {
        
        $send.hide();
        $notSend.hide();
        changeCheckedType($send, false);
        changeCheckedType($notSend, false);
        $refund_ind.prop('checked', false);

        let $checkedItem;

        if($(this).val() === '已送出') $checkedItem = $send;
        if($(this).val() === '未送出') {
            $checkedItem = $notSend;
            $refund_ind.prop('checked', true);
            $notSend.find('.condition_value.refund_ind').attr('disabled', false);
        }

        $checkedItem.show();
    })
}

function changeCheckedType($item) {
    $item.find('.condition').prop('checked', false);
    $item.find('.condition_value').attr('disabled', 'disabled');
}

function searchPageViewCoformEvent() {
    $alertViewcoform.find('.buttons').on('click', '.button', function () {
        const thisId = $(this).attr('id');
        if(thisId === 'Btn_print') {
            window.print();
        }
        if(thisId === 'Btn_cancel') {
            $alertViewcoform.hide();
            searchPageInitViewCoform();
        }
    })
}

function searchPageShowDataInViewCoform(data) {
    const viewTexts = $alertViewcoform.find('.viewText');
    for (let i = 0; i < viewTexts.length; i++) {
        const itemId = $(viewTexts[i]).attr('id');
        
        let id = itemId.slice(5,itemId.length);
        $(viewTexts[i]).text(data[id]);
    }
    $alertViewcoform.find('#View_sign_img').html(`<img src="${data.signature}" alt="sign">`);
}

function searchPageInitViewCoform() {
    const viewTexts = $alertViewcoform.find('.viewText');
    for (let i = 0; i < viewTexts.length; i++) {
        $(viewTexts[i]).text('');
    }
    $alertViewcoform.find('#View_sign_img').html('');
}

function searchPageViewCoform() {
    $search_coform.on('click', '.view.btn', function () {
        const $tr = $(this).parents('tr');
        const storeId = $tr.find('td[headers="order_id"]').text().substring(0,2);
        const trData = {
            amount: checkTdValue($tr.find('td[headers="amount"]').text()),
            auth_code: checkTdValue($tr.find('td[headers="auth_code"]').text()),
            auth_date: checkTdValue($tr.find('td[headers="auth_date"]').text()),
            bank: getBankName($tr.find('td[headers="bank"]').text()),
            card_exp: checkTdValue($tr.find('td[headers="card_exp"]').text()),
            card_holder: checkTdValue($tr.find('td[headers="card_holder"]').text()),
            card_num: formatCodeNum($tr.find('td[headers="card_num"]').text()),
            last3: checkTdValue($tr.find('td[headers="last3"]').text()),
            order_id: checkTdValue($tr.find('td[headers="order_id"]').text()),
            req_date: checkTdValue($tr.find('td[headers="req_date"]').text()),
            signature: $tr.data('sign'),
            storeName: checkTdValue(`${storeId} / ${$tr.find('td[headers="store_name"]').text()}`)
        }
        console.log(trData);
        searchPageShowDataInViewCoform(trData);
        showStoreTitle(storeId, $alertViewcoform);
        $alertViewcoform.show();
        $alertViewcoform.find('.alertMain').scrollTop(0);
    })
}

function checkTdValue(val) {
    return val === 'null' ? '' : val;
}

const bankList = {
    '004': '臺灣銀行',
    '005': '臺灣土地銀行',
    '006': '合作金庫商業銀行',
    '007': '第一商業銀行',
    '008': '華南商業銀行',
    '009': '彰化商業銀行',
    '011': '上海商業儲蓄銀行',
    '012': '台北富邦商業銀行',
    '013': '國泰世華商業銀行',
    '015': '中國輸出入銀行',
    '016': '高雄銀行',
    '017': '兆豐國際商業銀行',
    '021': '花旗(台灣)商業銀行',
    '048': '王道商業銀行',
    '050': '臺灣中小企業銀行',
    '052': '渣打國際商業銀行',
    '053': '台中商業銀行',
    '054': '京城商業銀行',
    '081': '滙豐(台灣)商業銀行',
    '101': '瑞興商業銀行',
    '102': '華泰商業銀行',
    '103': '臺灣新光商業銀行',
    '108': '陽信商業銀行',
    '118': '板信商業銀行',
    '147': '三信商業銀行',
    '803': '聯邦商業銀行',
    '805': '遠東國際商業銀行',
    '806': '元大商業銀行',
    '807': '永豐商業銀行',
    '808': '玉山商業銀行',
    '809': '凱基商業銀行',
    '810': '星展(台灣)商業銀行',
    '812': '台新國際商業銀行',
    '815': '日盛國際商業銀行',
    '816': '安泰商業銀行',
    '822': '中國信託商業銀行',
    '020': '日商瑞穗銀行',
    '022': '美商美國銀行',
    '023': '泰國盤谷銀行',
    '025': '菲律賓首都銀行',
    '028': '美商美國紐約梅隆銀行',
    '029': '新加坡大華銀行',
    '030': '美商道富銀行',
    '037': '法國興業銀行',
    '039': '澳商澳盛銀行',
    '072': '德商德意志銀行',
    '075': '香港商東亞銀行',
    '072': '美商摩根大通銀行',
    '076': '德商德意志銀行',
    '078': '新加坡商星展銀行',
    '082': '法商法國巴黎銀行',
    '083': '英商渣打銀行',
    '085': '新加坡商新加坡華僑銀行',
    '086': '法商東方匯理銀行',
    '092': '瑞士商瑞士銀行',
    '093': '荷蘭商安智銀行',
    '097': '美商富國銀行',
    '098': '日商三菱日聯銀行',
    '321': '日商三井住友銀行',
    '324': '美商花旗銀行',
    '325': '香港上海滙豐銀行',
    '326': '西班牙商西班牙對外銀行',
    '328': '法商法國外貿銀行',
    '380': '大陸商中國銀行股份有限公司',
    '381': '大陸商交通銀行股份有限公司',
    '382': '大陸商中國建設銀行股份有限公司',
}

function getBankName(id) {
    return bankList[id]
}