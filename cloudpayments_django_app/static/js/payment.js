const payments = new cp.CloudPayments({
    yandexPaySupport: false,
    applePaySupport: false,
    googlePaySupport: false,
    masterPassSupport: false,
    tinkoffInstallmentSupport: false
});

payments.oncomplete = (result) => {
    console.log('result', result);
}


const data = {
    CloudPayments: {
        recurrent: {
            interval: 'Month',
            period: 1,
        }
    }
};


payments.pay("charge", { // options
    publicId: publicId,
    accountId: 'user@example.com',
    description: 'Подписка CrocVPN',
    amount: subscriptionPrice,
    currency: 'RUB',
    skin: 'modern',
    invoiceId: 1234567,
    data: data
}).then((result) => {
    // Объект типа WidgetResult
    console.log('result', result);
});

