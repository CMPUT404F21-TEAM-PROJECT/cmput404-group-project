// Function that converts UTC time to local time, if post is older than a day, add the year, month and day, else just show the time.
export function utcToLocal(date){
    let parsedDate = new Date(date);
    let difference = new Date() - parsedDate;
    const day = 1000 * 60 * 60 * 24;
    const dateShortForm = parsedDate.toLocaleTimeString([], {
        hour: 'numeric',
        minute: 'numeric',
        hour12: true
      });
    const dateLongForm = parsedDate.toLocaleTimeString([], {
        year: 'numeric',
        month: 'long',
        day: 'numeric',
        hour: 'numeric',
        minute: 'numeric',
        hour12: true
    });
    return difference > day ? dateLongForm : dateShortForm; 
}