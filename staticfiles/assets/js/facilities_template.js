
function floatingRepairOrderTransaction(item){
    var csrfToken = document.querySelector('#csrfData').getAttribute('data-csrf')

    result = `
        <!-- Floating Labels Form -->
        <form class="row g-3" id="form-${item.random_item_code_id}">
            <input type="hidden" name="csrfmiddlewaretoken" value="${csrfToken}">
            
            <!-- HIDDEN DATA -->
            <div class="col-md-12" style="display:none;">
                <div class="form-floating">        
                    
                    <input type="text" class="form-control" id="itemcodeid" placeholder="Item Code ID" value="${item.random_item_code_id}" name="item_code_id">                         
                    <label for="itemcodeid">Item Code ID</label>
                </div>
            </div>
            
            <div class="col-md-12" style="display:none;">
                <div class="form-floating">        
                    <input type="text" class="form-control" id="custodianid" placeholder="Custodian ID" value="${item.custodian_id}" name="custodian_id">                         
                    <label for="itemcodeid">Custodian ID</label>
                </div>
            </div>

            <div class="col-md-12" style="display:none;">
                <div class="form-floating">        
                    <input type="text" class="form-control" id="itemnamedescid" placeholder="Item Name Desc. ID" value="${item.item_name_desc_id}" name="item_name_desc_id">                         
                    <label for="itemcodeid">Item Name Description ID</label>
                </div>
            </div>

            <div class="col-md-12">
                <div class="form-floating">
                    
                    <input type="text" class="form-control" id="floatingitemcode" placeholder="Item Code" value="${item.item_code}" name="item_code">
                    <label for="floatingitemcode">Item Code</label>
                </div>
            </div>
            <div class="col-md-12">
                <div class="form-floating">
                    <input type="text" class="form-control" id="floatingitems" placeholder="Items" value="${item.brand}" name="brand">
                    <label for="floatingitems">Items</label>
                </div>
            </div>

            <div class="col-md-12">
                <div class="form-floating">
                    <input type="text" class="form-control" id="floatingProblem" placeholder="Problem Encountered" name="problem_encountered">
                    <label for="floatingProblem">Problem Encountered</label>
                </div>
            </div>

            <div class="col-md-12">
                <div class="form-floating">
                    <input type="text" class="form-control" id="floatingRecepient" placeholder="Recepient" name="recepient">
                    <label for="floatingRecepient">Recepient</label>
                </div>
            </div>

            <div class="col-md-12">
                <div class="form-floating">
                    <input type="text" class="form-control" id="floatingDeliveredBy" placeholder="Delivered By" name="delivered_by">
                    <label for="floatingDeliveredBy">Delivered By</label>
                </div>
            </div>  

            <div class="col-md-12">
                <div class="form-floating">
                    <input type="text" class="form-control" id="floatingReceivedBy" placeholder="Received By" name="received_by">
                    <label for="floatingReceivedBy">Received By</label>
                </div>
            </div>  
  
            <div class="col-md-12">                                          
                <div class="form-floating">
                <input type="date" class="form-control" id="floatingDate" name="repair_date">
                <label for="floatingDate">Date</label>
                </div>
            </div>
          

            <div class="text-center">
        
            </div>   

            <div class="modal-footer">
                <button type="button" class="btn btn-secondary" data-bs-dismiss="modal" id="dismissID">Close</button>
                <button type="submit" class="btn btn-primary">Save</button>
            </div>   

        </form><!-- End floating Labels Form -->`

        
    return result

}

