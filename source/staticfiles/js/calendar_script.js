function visitDates() {
    const calendar = new Calendar("#calendar");
    const value = JSON.parse(document.getElementById('visitsData').textContent);
    calendar.el.querySelectorAll("td").forEach(function (day) {
        const studentInfoElement = document.getElementById('student-info');
        const currentStudentId = studentInfoElement.dataset.studentId;
        const currentCourseId = studentInfoElement.dataset.courseId;
        const date = new Date(day.dataset.date);
        const visit = value.find(visit => {
            const visitDate = new Date(visit.visit_date);
            return visitDate.getDate() === date.getDate() &&
                visitDate.getMonth() === date.getMonth() &&
                visitDate.getFullYear() === date.getFullYear() &&
                visit.student === parseInt(currentStudentId) &&
                visit.course === parseInt(currentCourseId);
        });
        day.classList.remove("is-viewing", "not-viewing");
        if (visit) {
            if (visit.is_currently_viewing) {
                day.classList.add("is-viewing");
            } else {
                day.classList.add("not-viewing");
            }
        day.style.width = "24px";
        day.style.height = "20px";
        day.style.paddingTop = "4px";
        day.style.marginTop = "19px";
        }
    });
}

document.addEventListener("DOMContentLoaded", function () {
    visitDates()
});

function Calendar(selector) {
    this.el = document.querySelector(selector);
    this.currentMonth = new Date();
    this.render();
}

Calendar.prototype.render = function () {
    this.el.innerHTML = "";

    const header = document.createElement("header");
    header.innerHTML = this.getMonthName(this.currentMonth)
    this.el.appendChild(header);

    let table = document.createElement("table");
    table.appendChild(this.createHeaderRow());
    table.appendChild(this.createDays());
    this.el.appendChild(table);
};

Calendar.prototype.createHeaderRow = function () {
  let headerRow = document.createElement("tr");
  let daysOfWeek = ["Пн", "Вт", "Ср", "Чт", "Пт", "С", "Вс"];

  for (let i = 0; i < daysOfWeek.length; i++) {
    let th = document.createElement("th");
    th.textContent = daysOfWeek[i];
      headerRow.appendChild(th);
  }

  return headerRow;
};

Calendar.prototype.getStartDay = function () {
  let startDay;
  let firstDay = new Date(this.currentMonth.getFullYear(), this.currentMonth.getMonth(), 1);
  let day = firstDay.getDay();
  startDay = (day === 0 ? 6 : day - 1);

  return startDay;
};

Calendar.prototype.createDays = function () {
  let firstDay = new Date(this.currentMonth.getFullYear(), this.currentMonth.getMonth(), 1);
  let lastDay = new Date(this.currentMonth.getFullYear(), this.currentMonth.getMonth() + 1, 0);
  let currentDate = new Date(firstDay);

  let daysTable = document.createElement("tbody");
  currentDate.setDate(currentDate.getDate() - this.getStartDay());

  while (currentDate <= lastDay) {
    let weekRow = document.createElement("tr");

    for (let i = 0; i < 7; i++) {
      let td = document.createElement("td");
      td.textContent = currentDate.getDate();
      td.setAttribute("data-date", currentDate.toISOString());
      td.classList.add("calendar-day");

      if (currentDate.getMonth() !== this.currentMonth.getMonth()) {
        td.classList.add("other-month");
      }

      if (this.isToday(currentDate)) {
        td.classList.add("today");
      }

      weekRow.appendChild(td);
      currentDate.setDate(currentDate.getDate() + 1);
    }

    daysTable.appendChild(weekRow);
  }

  return daysTable;
};


Calendar.prototype.getMonthName = function (date) {
  let months = [
      "Январь", "Февраль", "Март", "Апрель", "Май", "Июнь",
      "Июль", "Август", "Сентябрь", "Октябрь", "Ноябрь", "Декабрь"
  ];

  return months[date.getMonth()];
};

Calendar.prototype.isToday = function (date) {
  let today = new Date();
  return date.getDate() === today.getDate() &&
      date.getMonth() === today.getMonth() &&
      date.getFullYear() === today.getFullYear();
};

$(document).keydown(function(e) {
    if (e.keyCode === 13 && !e.shiftKey) {
        e.preventDefault();
        let commentContent = $("#commentForm textarea").val().trim();
        if (commentContent.length >= 2) {
            $("#commentForm").submit();
        }
    }
});
