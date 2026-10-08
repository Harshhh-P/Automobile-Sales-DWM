// ============================================================
// MOTORIQ - FRONTEND JAVASCRIPT
// ============================================================

const API_BASE = "http://127.0.0.1:5000/api";


// ============================================================
// CHART STORAGE
// ============================================================

const charts = {};


// ============================================================
// CHART COLORS
// ============================================================

const COLORS = [
    "#8B5CF6",
    "#6366F1",
    "#38BDF8",
    "#22C55E",
    "#FB923C",
    "#F87171",
    "#A78BFA",
    "#60A5FA",
    "#34D399",
    "#FBBF24",
    "#C084FC",
    "#818CF8"
];


// ============================================================
// API HELPER
// ============================================================

async function fetchAPI(endpoint) {

    try {

        const response = await fetch(API_BASE + endpoint);

        if (!response.ok) {
            throw new Error("API request failed");
        }

        return await response.json();

    } catch (error) {

        console.error("API Error:", endpoint, error);

        return [];
    }
}


// ============================================================
// FORMATTERS
// ============================================================

function formatNumber(value) {

    return Number(value || 0).toLocaleString("en-IN");
}


function formatCurrency(value) {

    return "$" + Number(value || 0).toLocaleString("en-US", {
        maximumFractionDigits: 0
    });
}


function formatCurrencyShort(value) {

    const number = Number(value || 0);

    if (number >= 1000000000) {
        return "$" + (number / 1000000000).toFixed(1) + "B";
    }

    if (number >= 1000000) {
        return "$" + (number / 1000000).toFixed(1) + "M";
    }

    if (number >= 1000) {
        return "$" + (number / 1000).toFixed(1) + "K";
    }

    return "$" + number.toFixed(0);
}


// ============================================================
// COMMON CHART OPTIONS
// ============================================================

function commonChartOptions() {

    return {

        responsive: true,

        maintainAspectRatio: false,

        animation: {
            duration: 700
        },

        plugins: {

            legend: {
                labels: {
                    color: "#A5A1B8",
                    padding: 14,
                    font: {
                        size: 11
                    }
                }
            },

            tooltip: {
                backgroundColor: "#111025",
                titleColor: "#F8FAFC",
                bodyColor: "#D9D5E3",
                borderColor: "#302B4D",
                borderWidth: 1
            }
        },

        scales: {

            x: {

                ticks: {
                    color: "#A5A1B8",
                    font: {
                        size: 10
                    }
                },

                grid: {
                    color: "rgba(48,43,77,0.35)"
                }
            },

            y: {

                ticks: {
                    color: "#A5A1B8",
                    font: {
                        size: 10
                    }
                },

                grid: {
                    color: "rgba(48,43,77,0.35)"
                }
            }

        }
    };
}


// ============================================================
// DESTROY OLD CHART
// ============================================================

function destroyChart(name) {

    if (charts[name]) {

        charts[name].destroy();

        charts[name] = null;
    }
}


// ============================================================
// LOAD DASHBOARD SUMMARY
// ============================================================

async function loadSummary() {

    const summary = await fetchAPI("/dashboard/summary");

    if (!Array.isArray(summary)) {

        document.getElementById("totalSales").textContent =
            formatNumber(summary.total_sales);

        document.getElementById("totalRevenue").textContent =
            formatCurrency(summary.total_revenue);

        document.getElementById("averageSale").textContent =
            formatCurrency(summary.average_sale);
    }


    const company = await fetchAPI("/dashboard/company-count");

    if (!Array.isArray(company)) {

        document.getElementById("totalCompanies").textContent =
            formatNumber(company.total_companies);
    }


    const dealer = await fetchAPI("/dashboard/dealer-count");

    if (!Array.isArray(dealer)) {

        document.getElementById("totalDealers").textContent =
            formatNumber(dealer.total_dealers);
    }
}


// ============================================================
// YEAR CHART
// ============================================================

async function loadYearChart() {

    const data = await fetchAPI("/dashboard/yearly-sales");

    if (!Array.isArray(data) || data.length === 0) {
        return;
    }

    destroyChart("year");

    const ctx = document
        .getElementById("yearChart")
        .getContext("2d");


    charts.year = new Chart(ctx, {

        type: "line",

        data: {

            labels: data.map(row => row.year),

            datasets: [{

                label: "Sales",

                data: data.map(row => row.sales),

                borderColor: "#8B5CF6",

                backgroundColor:
                    "rgba(139,92,246,0.15)",

                pointBackgroundColor: "#8B5CF6",

                pointBorderColor: "#8B5CF6",

                pointRadius: 4,

                pointHoverRadius: 6,

                fill: true,

                tension: 0.35
            }]
        },

        options: commonChartOptions()

    });
}


// ============================================================
// BODY STYLE PIE / DOUGHNUT CHART
// ============================================================

async function loadBodyStyleChart() {

    const data = await fetchAPI("/dashboard/body-styles");

    if (!Array.isArray(data) || data.length === 0) {
        return;
    }

    destroyChart("body");

    const ctx = document
        .getElementById("bodyStyleChart")
        .getContext("2d");


    charts.body = new Chart(ctx, {

        type: "doughnut",

        data: {

            labels: data.map(row => row.body_style),

            datasets: [{

                label: "Sales",

                data: data.map(row => row.sales),

                backgroundColor: COLORS.slice(
                    0,
                    data.length
                ),

                borderColor: "#17152A",

                borderWidth: 3,

                hoverOffset: 8
            }]
        },

        options: {

            responsive: true,

            maintainAspectRatio: false,

            cutout: "58%",

            plugins: {

                legend: {

                    position: "bottom",

                    labels: {

                        color: "#A5A1B8",

                        padding: 13,

                        boxWidth: 12,

                        font: {
                            size: 10
                        }
                    }
                },

                tooltip: {

                    backgroundColor: "#111025",

                    titleColor: "#F8FAFC",

                    bodyColor: "#D9D5E3",

                    borderColor: "#302B4D",

                    borderWidth: 1,

                    callbacks: {

                        label: function(context) {

                            const value =
                                context.raw || 0;

                            return " Sales: " +
                                Number(value).toLocaleString();
                        }
                    }
                }
            }
        }

    });
}


// ============================================================
// MONTH CHART
// ============================================================

async function loadMonthChart() {

    const data = await fetchAPI("/dashboard/monthly-sales");

    if (!Array.isArray(data) || data.length === 0) {
        return;
    }

    destroyChart("month");

    const labels = data.map(row =>
        `${row.month_name} ${row.year}`
    );


    const ctx = document
        .getElementById("monthChart")
        .getContext("2d");


    charts.month = new Chart(ctx, {

        type: "bar",

        data: {

            labels: labels,

            datasets: [{

                label: "Sales",

                data: data.map(row => row.sales),

                backgroundColor:
                    "rgba(56,189,248,0.65)",

                borderColor: "#38BDF8",

                borderWidth: 1,

                borderRadius: 5
            }]
        },

        options: {

            ...commonChartOptions(),

            plugins: {

                ...commonChartOptions().plugins,

                legend: {
                    display: false
                }
            }
        }

    });
}


// ============================================================
// TRANSMISSION CHART
// ============================================================

async function loadTransmissionChart() {

    const data = await fetchAPI("/dashboard/transmission");

    if (!Array.isArray(data) || data.length === 0) {
        return;
    }

    destroyChart("transmission");

    const ctx = document
        .getElementById("transmissionChart")
        .getContext("2d");


    charts.transmission = new Chart(ctx, {

        type: "doughnut",

        data: {

            labels: data.map(row => row.transmission),

            datasets: [{

                data: data.map(row => row.sales),

                backgroundColor: [
                    "#6366F1",
                    "#38BDF8",
                    "#22C55E",
                    "#FB923C"
                ],

                borderColor: "#17152A",

                borderWidth: 3,

                hoverOffset: 8
            }]
        },

        options: {

            responsive: true,

            maintainAspectRatio: false,

            cutout: "58%",

            plugins: {

                legend: {

                    position: "bottom",

                    labels: {

                        color: "#A5A1B8",

                        padding: 15,

                        boxWidth: 12,

                        font: {
                            size: 11
                        }
                    }
                }
            }
        }

    });
}


// ============================================================
// COMPANY CHART
// ============================================================

async function loadCompanyChart() {

    const data = await fetchAPI("/dashboard/companies");

    if (!Array.isArray(data) || data.length === 0) {
        return;
    }

    const topCompanies = data.slice(0, 10);

    destroyChart("company");

    const ctx = document
        .getElementById("companyChart")
        .getContext("2d");


    charts.company = new Chart(ctx, {

        type: "bar",

        data: {

            labels: topCompanies.map(row => row.company),

            datasets: [{

                label: "Revenue",

                data: topCompanies.map(row => row.revenue),

                backgroundColor: COLORS.slice(
                    0,
                    topCompanies.length
                ),

                borderRadius: 5
            }]
        },

        options: {

            ...commonChartOptions(),

            indexAxis: "y",

            plugins: {

                ...commonChartOptions().plugins,

                legend: {
                    display: false
                },

                tooltip: {

                    callbacks: {

                        label: function(context) {

                            return " Revenue: " +
                                formatCurrency(context.raw);
                        }
                    }
                }
            },

            scales: {

                x: {

                    ticks: {

                        color: "#A5A1B8",

                        callback: function(value) {
                            return formatCurrencyShort(value);
                        }
                    },

                    grid: {
                        color: "rgba(48,43,77,0.35)"
                    }
                },

                y: {

                    ticks: {
                        color: "#A5A1B8"
                    },

                    grid: {
                        display: false
                    }
                }
            }
        }

    });
}


// ============================================================
// REGION CHART
// ============================================================

async function loadRegionChart() {

    const data = await fetchAPI("/dashboard/regions");

    if (!Array.isArray(data) || data.length === 0) {
        return;
    }

    destroyChart("region");

    const ctx = document
        .getElementById("regionChart")
        .getContext("2d");


    charts.region = new Chart(ctx, {

        type: "bar",

        data: {

            labels: data.map(row => row.region),

            datasets: [{

                label: "Sales",

                data: data.map(row => row.sales),

                backgroundColor:
                    "rgba(139,92,246,0.65)",

                borderColor: "#8B5CF6",

                borderWidth: 1,

                borderRadius: 5
            }]
        },

        options: {

            ...commonChartOptions(),

            plugins: {

                ...commonChartOptions().plugins,

                legend: {
                    display: false
                }
            }
        }

    });
}


// ============================================================
// RENDER TABLE
// ============================================================

function renderTable(containerId, data) {

    const container =
        document.getElementById(containerId);


    if (!container) {
        return;
    }


    if (!Array.isArray(data) || data.length === 0) {

        container.innerHTML =
            `<p style="color:#A5A1B8;font-size:12px;">
                No data available.
            </p>`;

        return;
    }


    const columns = Object.keys(data[0]);


    let html = "<table><thead><tr>";


    columns.forEach(column => {

        let heading =
            column
                .replaceAll("_", " ")
                .replace(/\b\w/g, char =>
                    char.toUpperCase()
                );

        html += `<th>${heading}</th>`;
    });


    html += "</tr></thead><tbody>";


    data.forEach(row => {

        html += "<tr>";


        columns.forEach(column => {

            let value = row[column];


            if (
                column.includes("price") ||
                column.includes("revenue") ||
                column.includes("average") ||
                column.includes("sale")
            ) {

                if (
                    typeof value === "number" ||
                    !isNaN(value)
                ) {

                    value =
                        Number(value).toLocaleString(
                            "en-US",
                            {
                                maximumFractionDigits: 0
                            }
                        );
                }
            }


            html += `<td>${value ?? "-"}</td>`;
        });


        html += "</tr>";
    });


    html += "</tbody></table>";


    container.innerHTML = html;
}


// ============================================================
// LOAD VEHICLE SECTION
// ============================================================

async function loadVehicleSection() {

    const models =
        await fetchAPI("/vehicles/top-models");

    renderTable(
        "vehicleModelTable",
        models
    );


    const companies =
        await fetchAPI("/vehicles/companies");

    renderTable(
        "vehicleCompanyTable",
        companies
    );
}


// ============================================================
// LOAD DEALER SECTION
// ============================================================

async function loadDealerSection() {

    const dealers =
        await fetchAPI("/dealers/top");

    renderTable(
        "dealerTable",
        dealers
    );


    const regions =
        await fetchAPI("/regions/performance");

    renderTable(
        "dealerRegionTable",
        regions
    );
}


// ============================================================
// LOAD DICE FILTERS
// ============================================================

async function loadDiceFilters() {

    const regions =
        await fetchAPI("/dashboard/regions");

    const bodies =
        await fetchAPI("/dashboard/body-styles");

    const companies =
        await fetchAPI("/dashboard/companies");


    const regionSelect =
        document.getElementById("diceRegion");

    const bodySelect =
        document.getElementById("diceBody");

    const companySelect =
        document.getElementById("diceCompany");


    regions.forEach(row => {

        const option =
            document.createElement("option");

        option.value = row.region;

        option.textContent = row.region;

        regionSelect.appendChild(option);
    });


    bodies.forEach(row => {

        const option =
            document.createElement("option");

        option.value = row.body_style;

        option.textContent = row.body_style;

        bodySelect.appendChild(option);
    });


    companies.forEach(row => {

        const option =
            document.createElement("option");

        option.value = row.company;

        option.textContent = row.company;

        companySelect.appendChild(option);
    });
}


// ============================================================
// OLAP ROLL-UP
// ============================================================

async function runRollup() {

    const level =
        document.getElementById("rollupLevel").value;


    const data =
        await fetchAPI(
            `/olap/roll-up?level=${level}`
        );


    renderTable(
        "rollupResult",
        data
    );
}


// ============================================================
// OLAP DRILL-DOWN
// ============================================================

async function runDrilldown() {

    const year =
        document.getElementById("drillYear").value;


    const data =
        await fetchAPI(
            `/olap/drill-down?year=${year}`
        );


    renderTable(
        "drillResult",
        data
    );
}


// ============================================================
// OLAP SLICE
// ============================================================

async function runSlice() {

    const year =
        document.getElementById("sliceYear").value;


    const data =
        await fetchAPI(
            `/olap/slice?year=${year}`
        );


    renderTable(
        "sliceResult",
        data
    );
}


// ============================================================
// OLAP DICE
// ============================================================

async function runDice() {

    const year =
        document.getElementById("diceYear").value;

    const region =
        document.getElementById("diceRegion").value;

    const body =
        document.getElementById("diceBody").value;

    const company =
        document.getElementById("diceCompany").value;


    const params =
        new URLSearchParams();


    if (year) {
        params.append("year", year);
    }

    if (region) {
        params.append("region", region);
    }

    if (body) {
        params.append("body_style", body);
    }

    if (company) {
        params.append("company", company);
    }


    const data =
        await fetchAPI(
            `/olap/dice?${params.toString()}`
        );


    renderTable(
        "diceResult",
        data
    );
}


// ============================================================
// DATA MINING
// ============================================================

const miningDescriptions = {

    company:
        "Company-wise sales, revenue and average price.",

    model:
        "Top automobile models based on sales.",

    dealer:
        "Top dealers ranked by revenue.",

    region:
        "Regional sales performance.",

    "customer-gender":
        "Sales distribution by customer gender.",

    "customer-income":
        "Sales analysis by customer income group.",

    "vehicle-color":
        "Popular vehicle colors based on sales.",

    expensive:
        "Top 10 most expensive vehicle sales.",

    year:
        "Year-wise automobile sales analysis.",

    month:
        "Month-wise automobile sales analysis.",

    "company-region":
        "Company and region combined analysis."
};


async function runMining(type) {

    const endpoint =
        `/mining/${type}`;


    const data =
        await fetchAPI(endpoint);


    document.getElementById("miningTitle")
        .textContent =
        type
            .replaceAll("-", " ")
            .replace(/\b\w/g, char =>
                char.toUpperCase()
            );


    document.getElementById("miningDescription")
        .textContent =
        miningDescriptions[type] ||
        "Data mining analysis.";


    renderTable(
        "miningResult",
        data
    );
}


// ============================================================
// NAVIGATION
// ============================================================

function setupNavigation() {

    const navItems =
        document.querySelectorAll(
            ".nav-item[data-section]"
        );


    const sections =
        document.querySelectorAll(
            ".page-section"
        );


    navItems.forEach(item => {

        item.addEventListener(
            "click",
            function() {

                const sectionId =
                    this.dataset.section;


                navItems.forEach(nav =>
                    nav.classList.remove(
                        "active"
                    )
                );


                this.classList.add("active");


                sections.forEach(section =>
                    section.classList.remove(
                        "active"
                    )
                );


                const section =
                    document.getElementById(
                        sectionId
                    );


                if (section) {
                    section.classList.add(
                        "active"
                    );
                }


                updatePageTitle(sectionId);


                if (sectionId === "vehicles") {
                    loadVehicleSection();
                }


                if (sectionId === "dealers") {
                    loadDealerSection();
                }

            }
        );
    });
}


// ============================================================
// PAGE TITLES
// ============================================================

function updatePageTitle(sectionId) {

    const titles = {

        overview:
            "Dashboard Overview",

        olap:
            "OLAP Analysis",

        vehicles:
            "Vehicle Analysis",

        dealers:
            "Dealer & Region Analysis",

        mining:
            "Data Mining",

        reports:
            "Reports",

        about:
            "About Project"
    };


    document.getElementById("pageTitle")
        .textContent =
        titles[sectionId] ||
        "MotorIQ";
}


// ============================================================
// EVENT LISTENERS
// ============================================================

function setupEvents() {

    document
        .getElementById("rollupBtn")
        .addEventListener(
            "click",
            runRollup
        );


    document
        .getElementById("drillBtn")
        .addEventListener(
            "click",
            runDrilldown
        );


    document
        .getElementById("sliceBtn")
        .addEventListener(
            "click",
            runSlice
        );


    document
        .getElementById("diceBtn")
        .addEventListener(
            "click",
            runDice
        );


    document
        .querySelectorAll(
            "[data-mining]"
        )
        .forEach(button => {

            button.addEventListener(
                "click",
                () => {

                    runMining(
                        button.dataset.mining
                    );

                }
            );

        });
}


// ============================================================
// INITIAL LOAD
// ============================================================

async function initializeDashboard() {

    console.log(
        "MotorIQ dashboard loading..."
    );


    await loadSummary();

    await Promise.all([

        loadYearChart(),

        loadBodyStyleChart(),

        loadMonthChart(),

        loadTransmissionChart(),

        loadCompanyChart(),

        loadRegionChart(),

        loadDiceFilters()

    ]);


    setupNavigation();

    setupEvents();


    console.log(
        "MotorIQ dashboard loaded successfully."
    );
}


// ============================================================
// START APPLICATION
// ============================================================

document.addEventListener(
    "DOMContentLoaded",
    initializeDashboard
);