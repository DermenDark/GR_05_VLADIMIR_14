const initialData = [
    ["Иванов", "Иван", "Иванович", "100001", 1500],
    ["Петров", "Пётр", "Петрович", "100002", 2300],
    ["Иванов", "Иван", "Иванович", "100003", 2500],
    ["Сидоров", "Алексей", "Алексеевич", "100004", 800],
    ["Смирнова", "Анна", "Сергеевна", "100005", 5000],
    ["Петров", "Пётр", "Петрович", "100006", 3000],
    ["Козлов", "Дмитрий", "Олегович", "100007", 1200],
    ["Смирнова", "Анна", "Сергеевна", "100008", 750],
    ["Орлов", "Максим", "Игоревич", "100009", 4000],
    ["Иванов", "Иван", "Иванович", "100010", 500]
];

function renderAll(records, table) {
    table.innerHTML = "";

    records.forEach(client => {
        const data = client.getData();
        const row = document.createElement("tr");

        const values = [
            data.surname,
            data.firstName,
            data.patronymic,
            data.accountNumber,
            Number(data.deposit ?? 0).toFixed(2)
        ];

        values.forEach(value => {
            const cell = document.createElement("td");
            cell.textContent = value;
            row.appendChild(cell);
        });

        table.appendChild(row);
    });
}

function renderResult(records, result) {
    const groups = new Map();

    records.forEach(client => {
        const data = client.getData();

        const key = [
            data.surname,
            data.firstName,
            data.patronymic
        ].map(value => value.trim().toLowerCase()).join("|");

        if (!groups.has(key)) {
            groups.set(key, {
                name: `${data.surname} ${data.firstName} ${data.patronymic}`,
                count: 0,
                total: 0
            });
        }

        const group = groups.get(key);

        group.count++;
        group.total += Number(data.deposit);
    });

    const multipleClients = [...groups.values()]
        .filter(client => client.count > 1);

    result.innerHTML = "";

    if (multipleClients.length === 0) {
        result.textContent = "Клиентов с несколькими счетами не найдено.";
        return;
    }

    const list = document.createElement("ul");

    multipleClients.forEach(client => {
        const item = document.createElement("li");

        item.textContent =
            `${client.name}: счетов — ${client.count}, ` +
            `общая сумма — ${client.total.toFixed(2)}`;

        list.appendChild(item);
    });

    result.appendChild(list);
}


function ProtoPerson(surname = "", firstName = "", patronymic = "") {
    this.surname = surname;
    this.firstName = firstName;
    this.patronymic = patronymic;
}

ProtoPerson.prototype.getData = function () {
    return {
        surname: this.surname,
        firstName: this.firstName,
        patronymic: this.patronymic
    };
};

ProtoPerson.prototype.setData = function (surname, firstName, patronymic) {
    this.surname = surname;
    this.firstName = firstName;
    this.patronymic = patronymic;

    return this;
};

ProtoPerson.prototype.addFromForm = function (form, records) {
    const data = new FormData(form);
    const client = new this.constructor();

    client.setData(
        data.get("surname"),
        data.get("firstName"),
        data.get("patronymic"),
        data.get("accountNumber"),
        data.get("deposit")
    );

    records.push(client);
    form.reset();
};

ProtoPerson.prototype.showAll = function (records, table) {
    renderAll(records, table);
};

ProtoPerson.prototype.showResult = function (records, result) {
    renderResult(records, result);
};


function ProtoBankClient(
    surname = "",
    firstName = "",
    patronymic = "",
    accountNumber = "",
    deposit = 0
) {
    ProtoPerson.call(this, surname, firstName, patronymic);

    this.accountNumber = accountNumber;
    this.deposit = Number(deposit);
}

ProtoBankClient.prototype = Object.create(ProtoPerson.prototype);
ProtoBankClient.prototype.constructor = ProtoBankClient;

ProtoBankClient.prototype.getData = function () {
    return {
        ...ProtoPerson.prototype.getData.call(this),
        accountNumber: this.accountNumber,
        deposit: this.deposit
    };
};

ProtoBankClient.prototype.setData = function (
    surname,
    firstName,
    patronymic,
    accountNumber,
    deposit
) {
    ProtoPerson.prototype.setData.call(
        this,
        surname,
        firstName,
        patronymic
    );

    this.accountNumber = accountNumber;
    this.deposit = Number(deposit);

    return this;
};


const prototypeRecords = [];
const prototypeManager = new ProtoBankClient();

document.getElementById("prototypeForm").addEventListener("submit", function (event) {
    event.preventDefault();

    prototypeManager.addFromForm(this, prototypeRecords);

    prototypeManager.showAll(
        prototypeRecords,
        document.getElementById("prototypeTable")
    );

    prototypeManager.showResult(
        prototypeRecords,
        document.getElementById("prototypeResult")
    );
});


class Person {

    constructor(surname = "", firstName = "", patronymic = "") {
        this.surname = surname;
        this.firstName = firstName;
        this.patronymic = patronymic;
    }

    getData() {
        return {
            surname: this.surname,
            firstName: this.firstName,
            patronymic: this.patronymic
        };
    }

    setData(surname, firstName, patronymic) {
        this.surname = surname;
        this.firstName = firstName;
        this.patronymic = patronymic;

        return this;
    }

    addFromForm(form, records) {
        const data = new FormData(form);
        const client = new this.constructor();

        client.setData(
            data.get("surname"),
            data.get("firstName"),
            data.get("patronymic"),
            data.get("accountNumber"),
            data.get("deposit")
        );

        records.push(client);
        form.reset();
    }

    showAll(records, table) {
        renderAll(records, table);
    }

    showResult(records, result) {
        renderResult(records, result);
    }
}


class BankClient extends Person {

    constructor(
        surname = "",
        firstName = "",
        patronymic = "",
        accountNumber = "",
        deposit = 0
    ) {
        super(surname, firstName, patronymic);

        this.accountNumber = accountNumber;
        this.deposit = Number(deposit);
    }

    getData() {
        return {
            ...super.getData(),
            accountNumber: this.accountNumber,
            deposit: this.deposit
        };
    }

    setData(surname, firstName, patronymic, accountNumber, deposit) {
        super.setData(surname, firstName, patronymic);

        this.accountNumber = accountNumber;
        this.deposit = Number(deposit);

        return this;
    }
}


const classRecords = [];
const classManager = new BankClient();

document.getElementById("classForm").addEventListener("submit", function (event) {
    event.preventDefault();

    classManager.addFromForm(this, classRecords);

    classManager.showAll(
        classRecords,
        document.getElementById("classTable")
    );

    classManager.showResult(
        classRecords,
        document.getElementById("classResult")
    );
});


initialData.forEach(data => {
    const client = new ProtoBankClient();
    client.setData(...data);
    prototypeRecords.push(client);
});

initialData.forEach(data => {
    const client = new BankClient();
    client.setData(...data);
    classRecords.push(client);
});


prototypeManager.showAll(
    prototypeRecords,
    document.getElementById("prototypeTable")
);

prototypeManager.showResult(
    prototypeRecords,
    document.getElementById("prototypeResult")
);

classManager.showAll(
    classRecords,
    document.getElementById("classTable")
);

classManager.showResult(
    classRecords,
    document.getElementById("classResult")
);