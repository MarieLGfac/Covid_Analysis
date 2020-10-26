document.addEventListener('readystatechange', () => {
    console.log(document.readyState)
    if(document.readyState == 'interactive') {
        console.log(document.readyState)
    }
});