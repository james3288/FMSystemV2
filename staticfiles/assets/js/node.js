

class Card{
    constructor(title,container){
        this.title = title;
        this.container = container;
    }

    design = (title,body,button) => {
        let value = `
        <div class="card" style="width: 18rem;">
            <img src="..." class="card-img-top" alt="...">`
        value += `<div class="card-body">`
            if (title === true){
                value += `<h5 class="card-title">Card title</h5>`;
            }

            if (body === true){
                value += `<p class="card-text">Some quick example text to build on the card title and make up the bulk of the card's content.</p>`;
            }
            
            if (button === true){
                value += `<a href="#" class="btn btn-primary">Go somewhere</a>`
            }

        value += `</div>
        </div>
        `;

        return value;
    }

}


const card = new Card('Hello');
console.log(card.design(true,true,true));
