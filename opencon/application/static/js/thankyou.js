// ThankYou page is now being hosted by NationBuilder. Some information is being sent there in the URL and needs to be parsed using JavaScript.
// https://web.archive.org/web/20160527200317/http://stackoverflow.com/questions/979975/how-to-get-the-value-from-the-url-parameter#comment40513532_20336097
function urldecode(str) {
    return decodeURIComponent((str+'').replace(/\+/g, '%20'));
};
$(window).ready(function() {
    var url = window.location.search;
    var url = urldecode(url);
    // extract parameters
    var firstname = (url.split('firstname=')[1]||'').split('&')[0]
    var lastname = (url.split('lastname=')[1]||'').split('&')[0]
    var preferredname = (url.split('preferredname=')[1]||'').split('&')[0]
    var country = (url.split('country=')[1]||'').split('&')[0]
    var referral = (url.split('referral=')[1]||'').split('&')[0]
    // if no values are specified in the URL, set defaults
    var firstname = firstname ? firstname : 'Applicant';
    var lastname = lastname ? lastname : '';
    var country = country ? country : 'your country';
    var preferredname = preferredname ? preferredname : 'Applicant';
    var referral = referral ? referral : 'abc123';
    // .replace("[FirstName]", firstname) does only 1 replacement; use #regex with "/g" (global) flag
    // "[" and "]" need to be escaped
    $('#content').html($('#content').html().replace(/\[FirstName\]/g, firstname));
    $('#content').html($('#content').html().replace(/\[LastName\]/g, lastname));
    $('#content').html($('#content').html().replace(/\[PreferredName\]/g, preferredname));
    $('#content').html($('#content').html().replace(/\[Referral\]/g, referral));
});
