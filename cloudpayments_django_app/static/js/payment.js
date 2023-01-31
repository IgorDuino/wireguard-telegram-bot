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

const receipt = {
    Items: [//товарные позиции
        {
            label: 'Наименование товара 3', //наименование товара
            price: 300.00, //цена
            quantity: 3.00, //количество
            amount: 900.00, //сумма
            vat: 20, //ставка НДС
            method: 0, // тег-1214 признак способа расчета - признак способа расчета
            object: 0, // тег-1212 признак предмета расчета - признак предмета товара, работы, услуги, платежа, выплаты, иного предмета расчета
        }
    ],
    taxationSystem: 0, //система налогообложения; необязательный, если у вас одна система налогообложения
    email: 'user@example.com', //e-mail покупателя, если нужно отправить письмо с чеком
    phone: '', //телефон покупателя в любом формате, если нужно отправить сообщение со ссылкой на чек
    isBso: false, //чек является бланком строгой отчетности
    amounts: {
        electronic: 900.00, // Сумма оплаты электронными деньгами
        advancePayment: 0.00, // Сумма из предоплаты (зачетом аванса) (2 знака после запятой)
        credit: 0.00, // Сумма постоплатой(в кредит) (2 знака после запятой)
        provision: 0.00 // Сумма оплаты встречным предоставлением (сертификаты, др. мат.ценности) (2 знака после запятой)
    }
};

const data = { //содержимое элемента data
    CloudPayments: {
        CustomerReceipt: receipt, //чек для первого платежа
        recurrent: {
            interval: 'Month',
            period: 1,
            customerReceipt: receipt //чек для регулярных платежей
        }
    }
};

payments.pay("charge", { // options
    publicId: public_id,
    accountId: 'user@example.com',
    description: 'Оплата товаров в example.com',
    amount: 123000,
    currency: 'RUB',
    invoiceId: 1234567,
    data: data
}).then((result) => {
    // Объект типа WidgetResult
    console.log('result', result);
});

