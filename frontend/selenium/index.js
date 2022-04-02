const {Builder, By, Key, util} = require("selenium-webdriver");
async function example() {
  let driver = await new Builder().forBrowser("firefox").build();
  await driver.get("http://frontend404.herokuapp.com");
  await driver.findElement(By.name("q")).sendKeys("Selenium", Key.RETURN);
  driver.close();
}

example();