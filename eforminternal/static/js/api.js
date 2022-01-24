function getToken() {
    let result = {};
    $.ajax({
        url: 'https://event.smarter.com.tw/api/simplybook/login',
        type: 'post',
        data: JSON.stringify({
            account: "chatBot",
            keygen: "#5k4G4ji@2k!au4Fangcalaya$3"
        }),
        dataType: 'json',
        error: function (e) {
            console.log(e);
        },
        async: false,
        success: function (r) {
            result = r.token
        }
    })
    return result.toString()
}

function getData({ url, success, data, error }) {
    let type = data ? 'post' : 'get';
    $.ajax({
        url: 'http://18.183.236.5/api/' + url,
        type: type,
        contentType: 'application/json; charset=UTF-8',
        data: JSON.stringify(data),
        dataType: 'json',
        error: function (e) {
            console.log(e);
            console.log(`錯誤代碼: ${e.status} ${e.statusText} ${e.responseText}`);
            removeAlertMsg();
            alertMsg('wrong', `錯誤: ${e.status} 請聯繫總部`, e.responseText);
            if (typeof error === 'function') {
                error();
            }
        },
        success: function (r) {
            success(r);
        }
    })
}

function postData(url, data) {
    return fetch('http://18.183.236.5/api/' + url, {
        body: JSON.stringify(data),
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        }
    })
    .catch(error => console.error('Error:', error))
    .then(response => {
        console.log(response);
        if (response.status !== 200) {
            alert(`錯誤代碼: ${response.status} ${response.statusText}`)
            return false
        }
        response => response.json()
    })
    .then(tojson => console.log(tojson))
}

function deleteCashpyData({id, success}) {
    fetch('http://18.183.236.5/api/search/cashpymt/delete/' + id + '/cashPymtSearch', {
        method: 'delete'
    })
    .then(response =>
        response.json().then(json => {
            alertMsg('success', json);
            success(json);
        })
    )
    .catch(res => alertMsg('wrong', res));
}
