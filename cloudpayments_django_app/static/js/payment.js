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


payments.pay("ch    arge", {
    publicId: publicId,
    accountId: profileServerId,
    description: 'Подписка CrocVPN ' + subscriptionPeriod + ' дней',
    amount: subscriptionPrice,
    currency: 'RUB',
    skin: 'modern',
    email: '',
    requireEmail: true,
    data: {
        CloudPayments: {
            recurrent: {
                interval: 'Day',
                period: subscriptionPeriod,
            }
        }
    }
});
