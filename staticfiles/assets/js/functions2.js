class Dashboard {
    constructor() {
        this.data = {};
    }
  
    indexData=() => {
        return new Promise((resolve, reject) => {
        $.ajax({
          type: 'GET',
          url: "/dashboard",
          success: (response) => {
            this.data = response;
     
            const borrowed      = this.data.dashboard_data.borrowed;
            const vacant        = this.data.dashboard_data.vacant;
            const repaired      = this.data.dashboard_data.repaired;
            const updated_price = this.data.updated_price; 
            const defective     = this.data.dashboard_data.defective;
            
            const result = {
                borrowed: borrowed,
                vacant: vacant,
                repaired: repaired,
                defective: defective,
                updated_price: updated_price
            }

            resolve(result);
            
          },
          error: (response) => {
            reject(new Error("An error occurred!"));
          }
        });
      });
    }
}