export default {
    getDatesBetween(startDate, endDate, includeStartDate, includeEndDate) {
        var dates = [];
        var currentDate = new Date(startDate);
        var endDate = new Date(endDate);

        if (!includeStartDate) {
            currentDate.setDate(currentDate.getDate() + 1);
        }

        if (!includeEndDate) {
            endDate.setDate(endDate.getDate() - 1);
        }

        while (currentDate <= endDate) {
            dates.push(new Date(currentDate));
            currentDate.setDate(currentDate.getDate() + 1);
        }
        return dates;
    },
    convertTimeTo12HourClock(time) {
        var hours24h = +time.substr(0, 2);
        var hours12h = (hours24h % 12) || 12;
        var extension = hours24h < 12 ? "am" : "pm";
        return hours12h + time.substr(2, 3) + " " + extension;
    }
}