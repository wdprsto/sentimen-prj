let i = 1;
const dict = {};
const like_regex = /\b(\d+) Like|Likes\b/;
const retweet_regex = /\b(\d+) Retweet|Retweets\b/;
const reply_regex = /\b(\d+) Repl(ies|y)\. Reply\b/;
const time_regex = /\btime datetime=\"(.*?)\">\b/;
const status_regex = /\b\/status\/(\d+)\b/;

function loop() {
  setTimeout(function () {
    window.scrollBy(0, 1000);
    let elements = document.querySelectorAll('[data-testid=tweet]');
    for (let index = 0; index < elements.length; index++) {
      try {
        let reply = elements[index].innerHTML.match(reply_regex);
        let like = elements[index].innerHTML.match(like_regex);
        let retweet = elements[index].innerHTML.match(retweet_regex);
        let time = elements[index].innerHTML.match(time_regex);
        let status = elements[index].innerHTML.match(status_regex);
        dict[elements[index].innerText.split("\n")[1].concat("-" + time[1])] = {
          "like": `${like[1]}`,
          "reply": `${reply[1]}`,
          "retweet": `${retweet[1]}`,
          "time": `${time[1]}`,
          "username": `${elements[index].innerText.split("\n")[1]}`,
          "text": `${elements[index].querySelector('[data-testid=tweetText]').innerText}`,
          "status": `${status[1]}`
        };
      } catch (error) {
        console.log(error);
        throw new Error(error);
      }
    }
    i++;
    if (i < 100000) {
      loop();
    }
  }, 500)
}
loop();