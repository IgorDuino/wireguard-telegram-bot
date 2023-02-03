const payments = new cp.CloudPayments({
    yandexPaySupport: true,
    applePaySupport: false,
    googlePaySupport: false,
    masterPassSupport: false,
    tinkoffInstallmentSupport: false,
});

payments.oncomplete = (result) => {
    console.log('result', result);
}


payments.pay("charge", {
    publicId: publicId,
    accountId: uid,
    description: 'Подписка CrocVPN 1 месяц',
    amount: subscriptionPrice,
    currency: 'RUB',
    skin: 'modern',
    data: {
        CloudPayments: {
            recurrent: {
                interval: 'Month',
                period: 1,
            }
        }
    }
});
