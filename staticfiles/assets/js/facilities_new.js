class Facilities {
  fac_data = (category, visible, cardbody, csrf_token) => {
    $.ajax({
      type: "GET",
      url: `/facilities_json/${category}/${visible}`,
      success: function (response) {
        let a = ``;

        function modalForm(item) {
          let modal = "";
          modal += `
                    <div class="modal-dialog modal-dialog-scrollable">
                        <div class="modal-content">
                            <div class="modal-header">
                                <h5 class="modal-title">Create Repair Order ${item.item_code}</h5>
                                <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                            </div>
                        
                            <!-- old buttons here -->
                        </div> 
                    </div>`;
          return modal;
        }

        response.fac_data.forEach((fac) => {
          a += `
                <div id='csrfData' data-csrf='${csrf_token}'></div>
                <!-- main title -->
                <h5 class="card-title">${
                  response.category
                } <span> | Today</span></h5>
                <!-- main title -->
                
                <!-- main sub -->
                <div class="card info-card customers-card" style="padding:5px 20px 5px 20px !important;">    
                    <!-- heading -->

                    <!-- first row -->
                    <div class="row">
                        <!-- row inside first row -->
                        <div class="container-fluid">

                            <!-- first row => 1 -->
                            <div class="row">

                                <!-- first row => left column -->
                                <div class="col-lg-4 col-md-4 col-sm-12 p-1">
                                    <div class="card" style="margin-bottom:20px !important;">
                                        <div class="card-body pt-3">
                                            <img src="${
                                              fac.img
                                            }" class="img-fluid rounded-start" alt="..." onerror="this.src='/staticfiles/assets/img/coming_soon.jpg'">
                                        </div>
                                    </div>
                                </div>
                                <!-- end first row => left colun -->


                                <!-- first row => right column -->
                                <div class="col-lg-8 col-md-8 p-1"> 

                                    <!-- CARD 1 -->
                                    <div class ="card" style="margin-bottom:20px !important">    
                                        <div class="card-header bg-light fs-4">
                                            ${fac.item_code}
                                        </div>
                                        <div class="card-body p-3">            
                    
                                            <div class="card-title p-0"><i class="ri-checkbox-multiple-fill"></i> 
                                                ${fac.item_name} - ${fac.brand}
                                            </div>
                                            <div class="card-title p-1 fs-6 text-white ${
                                              fac.status_served_name == "Serve"
                                                ? "badge bg-success"
                                                : fac.status_served_name ==
                                                  "Disposed"
                                                ? "badge bg-danger"
                                                : fac.status_served_name ==
                                                  "For Disposal"
                                                ? "badge bg-danger"
                                                : fac.status_served_name ==
                                                  "Vacant"
                                                ? "badge bg-warning"
                                                : ""
                                            }">
                                                ${fac.status_served_name}
                                            </div>

                                            <div class="card-title p-1 fs-6 text-white badge bg-info">
                                                ${fac.custodian_name}
                                            </div>

                                            <div class="card-title p-1 fs-6 text-white ${
                                              fac.repair_status == "Repaired"
                                                ? "badge bg-success"
                                                : fac.repair_status ==
                                                  "On-going Repair"
                                                ? "badge bg-danger"
                                                : ""
                                            }">
                                                ${fac.repair_status}
                                            </div> 
                                        </div>
                                    </div>
                                    <!-- END CARD 1 -->

                                    <!-- CARD 2 -->
                                    <div class ="card" style="margin-bottom:20px !important;">    
                                        <div class="card-header bg-light fs-4">
                                            PACKAGES:
                                        </div>
                                        <div class="card-body p-3">            
                                            <ul class="list-group">`;

          response.packages.forEach((sub) => {
            if (sub.item_code == fac.item_code) {
              a += `          <li class="list-group-item p-1">
                                                        <i class="ri-arrow-right-s-fill text-success"></i> 
                                                        <span class="${
                                                          sub.status_served_name ==
                                                          "Serve"
                                                            ? "badge bg-success"
                                                            : sub.status_served_name ==
                                                              "Disposed"
                                                            ? "badge bg-danger"
                                                            : sub.status_served_name ==
                                                              "For Disposal"
                                                            ? "badge bg-danger"
                                                            : sub.status_served_name ==
                                                              "Vacant"
                                                            ? "badge bg-warning"
                                                            : ""
                                                        }">${
                sub.status_served_name
              } | ${sub.borrowed_for}</span>
                                                        <span class="">
                                                            <a href="#" id="subitem_${
                                                              sub.subitems_id
                                                            }" class="card-title" data-bs-toggle="modal" data-bs-target="#modalDialogScrollable" onclick="GetSubItemHistory('subitem_${
                sub.subitems_id
              }'); return false;">${sub.item_name} - ${sub.brand}</a>
                                                        </span>
                                                    </li>`;
            }
          });
          a += `   </ul>
                                   
                                        </div>
                                    </div>
                                    <!-- END CARD 2 -->
                                    
                                    <!-- CARD 3 -->
                                    <div class ="card" style="margin-bottom:20px !important;">    
                                        <div class="card-header bg-light fs-4">
                                            DETAILS:
                                        </div>
                                        <div class="card-body p-3">        
                                            <ul class="list-group" id="packagesid">
                                                <li class="list-group-item li_a"><small><b class="card-title myHeader"><i class="ri-file-settings-fill text-info"></i>
                                                        Maintenance Schedule:</b></small>
                                                    <ul class="list-group">          
                                                        <li class="list-group-item p-1">
                                                            <i class="ri-arrow-right-s-fill text-info"></i> 
                                                            <span class="badge bg-info">Date Schedule</span>
                                                            <b class="text-primary" style="color: #012970 !important; font-size: 13px;">
                                                                ${fac.date_schedule_final}
                                                            </b>
                                                        </li>    
                                                        <li class="list-group-item p-1">
                                                            <i class="ri-arrow-right-s-fill text-info"></i> 
                                                            <span class="badge bg-info">Last Date Schedule</span>
                                                            <b class="text-primary" style="color: #012970 !important; font-size: 13px;">
                                                                ${fac.last_date_maint}
                                                            </b>
                                                        </li>                     
                                                    </ul>
                                                </li>

                                                <li class="list-group-item li_a"><small><b class="card-title myHeader">Information:</b></small>
                                                    <ul class="list-group">          
                                                        <li class="list-group-item p-1">
                                                            <i class="ri-arrow-right-s-fill text-info"></i> 
                                                            <span class="badge bg-info">Location</span>
                                                            <b class="text-primary" style="color: #012970 !important; font-size: 13px;">
                                                                ${fac.location} / ${fac.borrowed_for}
                                                            </b>
                                                        </li> 
                                                        <li class="list-group-item p-1">
                                                            <i class="ri-arrow-right-s-fill text-info"></i> 
                                                            <span class="badge bg-info">Date Borrowed</span>
                                                            <b class="text-primary" style="color: #012970 !important; font-size: 13px;">
                                                                ${fac.date_borrowed}
                                                            </b>
                                                        </li>  
                                                        <li class="list-group-item p-1">
                                                            <i class="ri-arrow-right-s-fill text-info"></i> 
                                                            <span class="badge bg-info">Aquisition Date</span>
                                                            <b class="text-primary" style="color: #012970 !important; font-size: 13px;">
                                                                ${fac.acquisition_date}
                                                            </b>
                                                        </li>       
                                                        <li class="list-group-item p-1">
                                                            <i class="ri-arrow-right-s-fill text-info"></i> 
                                                            <span class="badge bg-info">RS No</span>
                                                            <b class="text-primary" style="color: #012970 !important; font-size: 13px;">
                                                                ${fac.rs_no}
                                                            </b>
                                                        </li>   
                                                        <li class="list-group-item p-1">
                                                            <i class="ri-arrow-right-s-fill text-info"></i> 
                                                            <span class="badge bg-info">BS No</span>
                                                            <b class="text-primary" style="color: #012970 !important; font-size: 13px;">
                                                                ${fac.bs_no}
                                                            </b>
                                                        </li>  
                                                        <li class="list-group-item p-1">
                                                            <i class="ri-arrow-right-s-fill text-info"></i> 
                                                            <span class="badge bg-info">Serial No</span>
                                                            <b class="text-primary" style="color: #012970 !important; font-size: 13px;">
                                                                ${fac.serial_no}
                                                            </b>
                                                        </li>                         

                                                    </ul>
                                                </li>
                                            </ul>
                                        </div>
                                    </div>   
                                    <!-- END CARD 3 -->

                                    <!-- BUTTONS -->
                                    <div class ="card">                                   
                                        <div class="card-body p-3">    
                                            <div class="row">
                                                <div class="col-lg-4">                                           
                                                    <a class="btn btn-outline-primary mb-2" id="cro_id" style="width:100% !important" data-bs-toggle="modal" data-bs-target="#modal_cro_id_${fac.item_code}">Create Repair Order</a>  
                                                </div>  
                                                <div class="col-lg-4">
                                                    <a class="btn btn-primary mb-2" style="width:100% !important" href="/repair_order_history/desktop/DC-44">Repair Order History <span class="badge bg-white text-primary">0</span></a>
                                                
                                                </div>
                                                <div class="col-lg-4">
                                                    <a class="btn btn-primary mb-2" style="width:100% !important" href="/borrower_history/DC-44">Borrower History <span class="badge bg-white text-primary">0</span></a>
                                                </div>
                                            </div>
                                        </div>
                                    </div> 
                                    <!-- END BUTTONS -->

                                </div>
                                <!-- end first row => right column -->                  

                            </div>
                            <!-- end first row => 1 -->

                        </div>
                        <!-- end row inside first row -->
                    </div>
                    <!-- end first row -->
                    <!-- end heading -->
                    </div> <!-- end 2nd row -->
                </div>
                <!-- end main sub -->
                `;

          a += `
            <!-- modal for repairorder -->
            <div class="modal fade" id="modal_cro_id_${
              fac.item_code
            }" tabindex="-1">
                ${modalForm(fac)}
            </div>
            <!-- end modal for repairder -->
            `;
        });

        cardbody.innerHTML = a;

        // set attributes in a href

        const croid = document.getElementById("cro_id");
        const modal = document.getElementById("modal_cro_id");

        // croid.setAttribute('data-bs-toggle','modal');
        // croid.setAttribute('data-bs-target','#modal_cro_id');
      },
      error: function (error) {
        console.log(error);
      },
    });
  };
}

// CLASS FOR FACILITIES NEW
class RowStyle {
  constructor(cardbody, csrf_token) {
    this.cardbody = cardbody;
    this.csrf_token = csrf_token;
    this.subIds = [];
  }

  // EVENTS FOR REPAIR ORDER SAVE
  AddEventRepairOrderSave = (formBtn, fac) => {
    formBtn?.addEventListener("submit", function (event) {
      event.preventDefault();
      console.log(fac);
      var wowAlert = document.getElementById(
        `wowAlertID-${fac.random_item_code_id}`
      );

      // check if some textfield are empty
      var inputFields = document.querySelectorAll(
        `#form-${fac.random_item_code_id} input`
      );

      // Convert the NodeList to an array
      var inputArray = Array.from(inputFields);

      // Log the array of input fields
      // console.log(inputArray);

      // Check if any input field is empty
      var isEmpty = inputArray.some(function (input) {
        return input.value.trim() === ""; // Trim to handle whitespace
      });

      // if field is empty
      if (isEmpty) {
        console.log("At least one input field is empty.");
        wowAlert.textContent = "Some input fields are empty.";
        wowAlert.style.display = "block";
      } else {
        var wowAlert1 = document.getElementById(
          `wowAlertID-${fac.random_item_code_id}`
        );
        console.log("All input fields are filled.");
        wowAlert1.style.display = "none";

        const formData = new FormData(formBtn);
        fetch("/repair/", {
          method: "POST",
          headers: {
            "X-CSRFToken": getCSRFToken(), // Include CSRF token for security (see step 3)
          },
          body: formData,
        })
          .then(function (response) {
            // Process the response from the Django view if needed

            location.reload(true);
            var repairpage_url =
              "/under-repair/under-repair-items/" + fac.item_code;
            window.location.href = repairpage_url;
          })
          .catch(function (error) {
            console.log("Error:", error);
          });
      }
    });
  };
  // END EVENTS FOR REPAIR ORDER SAVE

  get_packages = (packages, item_code) => {
    let pack = "";

    packages.forEach((sub) => {
      if (sub.item_code == item_code) {
        pack += `<li class="list-group-item p-1">
                            <i class="ri-arrow-right-s-fill text-success"></i> 
                            <span class="${
                              sub.status_served_name == "Serve"
                                ? "badge bg-success"
                                : sub.status_served_name == "Disposed"
                                ? "badge bg-danger"
                                : sub.status_served_name == "For Disposal"
                                ? "badge bg-danger"
                                : sub.status_served_name == "Vacant"
                                ? "badge bg-warning"
                                : ""
                            }">${sub.status_served_name} | ${
          sub.borrowed_for
        }</span>
                            <span class="">
                                <a href="#" id="subitem_${
                                  sub.subitems_id
                                }" class="card-title" data-bs-toggle="modal" data-bs-target="#PackageModal">${
          sub.item_name
        } - ${sub.brand}</a>
                            </span>  
                        </li>`;
        // sub packages modal

        // end sub packages modal
      }
    });
    return pack;
  };

  modalForm = (fac) => {
    // var csrfToken = document.querySelector('#csrfData').getAttribute('data-csrf');
    let modal = "";
    modal += `
                <div class="modal-dialog modal-dialog-scrollable">
                    <div class="modal-content">
                        <div class="modal-header">
                            <h5 class="modal-title">Create Repair Order</h5>
                            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>                        
                        </div>       
                        <div class="modal-body">
                            <!-- Floating Labels Form -->
                            <form class="row g-3" id="form-${fac.random_item_code_id}">
                                <input type="hidden" name="csrfmiddlewaretoken" value="${this.csrf_token}">
                                
                                <!-- HIDDEN DATA -->
                                <div class="col-md-12" style="display:none;">
                                    <div class="form-floating">        
                                        
                                        <input type="text" class="form-control" id="itemcodeid" placeholder="Item Code ID" value="${fac.random_item_code_id}" name="item_code_id">                         
                                        <label for="itemcodeid">Item Code ID</label>
                                    </div>
                                </div>
                                
                                <div class="col-md-12" style="display:none;">
                                    <div class="form-floating">        
                                        <input type="text" class="form-control" id="custodianid" placeholder="Custodian ID" value="${fac.custodian_id}" name="custodian_id">                         
                                        <label for="itemcodeid">Custodian ID</label>
                                    </div>
                                </div>
                    
                                <div class="col-md-12" style="display:none;">
                                    <div class="form-floating">        
                                        <input type="text" class="form-control" id="itemnamedescid" placeholder="Item Name Desc. ID" value="${fac.item_name_desc_id}" name="item_name_desc_id">                         
                                        <label for="itemcodeid">Item Name Description ID</label>
                                    </div>
                                </div>
                    
                                <div class="col-md-12">
                                    <div class="form-floating">
                                        
                                        <input type="text" class="form-control" id="floatingitemcode" placeholder="Item Code" value="${fac.item_code}" name="item_code">
                                        <label for="floatingitemcode">Item Code</label>
                                    </div>
                                </div>
                                <div class="col-md-12">
                                    <div class="form-floating">
                                        <input type="text" class="form-control" id="floatingitems" placeholder="Items" value="${fac.brand}" name="brand">
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

                                <div class="col-md-12">
                                    <div class="form-floating">
                                    <input type="text" class="form-control" id="floatingContactNumber" placeholder="Contact Number" name="contact_number">
                                    <label for="floatingContactNumber">Contact Number</label>
                                    </div>
                                </div>

                                <div class="col-md-12">
                                    <div class="alert alert-warning alert-dismissible fade show" role="alert" id="wowAlertID-${fac.random_item_code_id}" style="display:none;">    
                                    </div> 
                                </div>
                                              
                                <div class="modal-footer">
                                    <button type="button" class="btn btn-secondary" data-bs-dismiss="modal" id="dismissID">Close</button>
                                    <button type="submit" class="btn btn-primary">Save</button>
                                </div>   
                    
                            </form><!-- End floating Labels Form -->
                        </div>                       
                    </div> 
                </div>`;
    return modal;
  };

  card1_left_col = (fac) => {
    const repair_order_history_url =
      "/under-repair/under-repair-items/" +
      slugify(fac.item_code).toUpperCase();
    const borrower_history_url =
      "/borrower_history/" + slugify(fac.item_code).toUpperCase();

    let col = `
        <div class = "col-lg-4 col-xs-12">
            <div class ="card" style="margin-bottom:20px !important">    
                <div class="card-body pt-3 myHover" id="item_pic_id">
                    <img src="${fac.img}" class="img-fluid rounded-start" style="object-fit: scale-down !important;" alt="..." onerror="this.src='/staticfiles/assets/img/coming_soon.jpg'">
                    <div class="overlay2">
                        <div class="text">ADFIL PROPERTY</div>
                    </div>
                </div>
                <div class="card-footer">
                    <div class="row p-2">
                        <div class="col-lg-12 p-1">
                            <button type="button" class="btn btn-success" style="width:100% !important;" data-bs-toggle="modal" data-bs-target="#modal_cro_id_${fac.item_code}" id="createRepairOrderBtn_${fac.item_code}">Create Repair Order</button>                             
                        </div>                      
                        <div class="col-lg-12 p-1">
                            <a href="${repair_order_history_url}" class="btn btn-primary" style="width:100% !important;"> Repair Order History <span class="badge bg-white text-primary"> ${fac.no_of_repair_history}</span></a>                             
                        </div>
                        <div class="col-lg-12 p-1">
                            <a href="${borrower_history_url}" class="btn btn-primary" style="width:100% !important;">Borrower History <span class="badge bg-white text-primary"> ${fac.no_of_borrowed}</span></a>                             
                        </div>
                    </div>          
                </div>
            </div>         
        </div>
        `;
    return col;
  };

  card1_right_col = (fac) => {
    let col = `
        <div class = "col-lg-8 col-xs-12">
            <!-- top -->
            <div class ="card" style="margin-bottom:20px !important;" id="top_right_id">                 
                <div class="card-header bg-light fs-4">
                    ${fac.item_code}
                </div>
                <div class="card-body p-3">            

                    <div class="card-title p-0"><i class="ri-checkbox-multiple-fill"></i> 
                        ${fac.item_name} - ${fac.brand}
                    </div>
                    <div class="card-title p-1 fs-6 text-white ${
                      fac.status_served_name == "Serve"
                        ? "badge bg-success"
                        : fac.status_served_name == "Defective - Disposed"
                        ? "badge bg-danger"
                        : fac.status_served_name == "Defective - For Disposal"
                        ? "badge bg-danger"
                        : fac.status_served_name == "Vacant"
                        ? "badge bg-warning"
                        : fac.status_served_name == "Defective - Serve"
                        ? "badge bg-secondary"
                        : fac.status_served_name == "Functional - Serve"
                        ? "badge bg-success"
                        : fac.status_served_name == "Disposed"
                        ? "badge bg-danger"
                        : fac.status_served_name == "Lost Item"
                        ? "badge bg-secondary"
                        : ""
                    }">
                        ${fac.status_served_name}
                    </div>

                    <div class="card-title p-1 fs-6 text-white badge bg-info">
                        ${fac.custodian_name}
                    </div>

                    <div class="card-title p-1 fs-6 text-white ${
                      fac.repair_status == "Repaired"
                        ? "badge bg-success"
                        : fac.repair_status == "On-going Repair"
                        ? "badge bg-danger"
                        : fac.repair_status == "Defective"
                        ? "badge bg-secondary"
                        : ""
                    }">
                        ${fac.repair_status}
                    </div> 
                
                    <ul class="list-group">          
                        <li class="list-group-item p-1">
                            <i class="ri-arrow-right-s-fill text-info"></i> 
                            <span class="card-title" style="font-size:14px !important;">
                                Date Borrowed: ${fac.date_borrowed}
                            </span>
                            
                        </li>                                         
                        <li class="list-group-item p-1">
                            <i class="ri-arrow-right-s-fill text-info"></i> 
                            <span class="card-title" style="font-size:14px !important;">
                                Aquisition Date: ${fac.acquisition_date}
                            </span>                                     
                        </li>
                        <li class="list-group-item p-1">
                            <i class="ri-arrow-right-s-fill text-info"></i> 
                            <span class="card-title" style="font-size:14px !important;">
                                Project: ${fac.borrowed_for}
                            </span>                                     
                        </li>            
                        <li class="list-group-item p-1">
                            <i class="ri-arrow-right-s-fill text-info"></i> 
                            <span class="card-title" style="font-size:14px !important;">
                                Location: ${fac.location}
                            </span>                                     
                        </li>            
                        <li class="list-group-item p-1">
                            <i class="ri-arrow-right-s-fill text-info"></i> 
                            <span class="card-title" style="font-size:14px !important;">
                                RS No: ${fac.rs_no}
                            </span>                                     
                        </li>
                        <li class="list-group-item p-1">
                            <i class="ri-arrow-right-s-fill text-info"></i> 
                            <span class="card-title" style="font-size:14px !important;">
                                Serial No: ${fac.serial_no}
                            </span>                                     
                        </li>
                        <li class="list-group-item p-1">
                            <i class="ri-arrow-right-s-fill text-info"></i> 
                            <span class="card-title" style="font-size:14px !important;">
                                BS No: ${fac.bs_no}
                            </span>                                     
                        </li>
                        <li class="list-group-item p-1">
                            <i class="ri-arrow-right-s-fill text-info"></i> 
                            <span class="card-title" style="font-size:14px !important;">
                                Maintenance Schedule: ${
                                  fac.date_schedule_final
                                } 
                            </span>                                     
                        </li>
                        <li class="list-group-item p-1">
                            <i class="ri-arrow-right-s-fill text-info"></i> 
                            <span class="card-title" style="font-size:14px !important;">
                                Last Date Maintenance Schedule: ${
                                  fac.last_date_maint
                                } 
                            </span>                                     
                        </li>
                    </ul>
                </div>

            </div>
            <!-- end top -->

        </div>
        `;
    return col;
  };

  async PackageHistoryModal() {
    let a = ``;
    a = `
        <!-- Modal For Package History-->
        <div class="modal fade" id="PackageModal" tabindex="-1">
            <div class="modal-dialog modal-dialog-scrollable">
                <div class="modal-content">
                    <div class="modal-header">
                    <h5 class="modal-title"><b class="card-title">SUB-ITEM BORROWED HISTORY</b></h5>
                    <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                    </div>
                    <div class="modal-body">
                        <div class="list-group" id="SubItemListId">                                                    
                        </div>
                    </div>
                    <div class="modal-footer">
                    <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
            
                    </div>
                </div>
            </div>
        </div>
        <!-- End Modal For Package History-->
        `;

    this.cardbody.innerHTML += a;
  }

  design = (fac, packages) => {
    //execute design here...

    let aa = `
        <div class="alert alert-info alert-dismissible fade show" role="alert" id="fiid" style="display:none">
            5 items has been found...
        </div>`;

    let a = ``;
    let title = `<h5 class="card-title">${fac.category} <span> | served ${fac.time_ago} ago</span></h5>`;
    let card1 = "";

    card1 = `
        <!-- CARD 1 -->
        <div class="container-fluid p-0">
            <div class="row">
                <!-- column left -->
                    ${this.card1_left_col(fac)}
                <!-- end column left -->

                <!-- column right -->
                    ${this.card1_right_col(fac)}
                <!-- end column right -->      

            </div>
        </div>
        <!-- END CARD 1 -->
        `;

    this.cardbody.innerHTML += aa;
    this.cardbody.innerHTML += title;
    this.cardbody.innerHTML += card1;

    // card 2 | packages for Desktop and Laptop
    if (fac.category == "Desktop") {
      let b = this.get_packages(packages, fac.item_code);
      let card2 = "";
      card2 = `
            <div class ="card" style="margin-bottom:20px !important;">    
                <div class="card-header bg-light fs-4">
                    PACKAGES:
                </div>
                <div class="card-body p-3">            
                    <ul class="list-group">
                        ${b}
                    </ul>                               
                </div>
            </div>
            `;

      this.cardbody.innerHTML += card2;
      // end card 2 | packages for Desktop and Laptop
    }

    // repairorder modal
    let card3 = "";
    card3 = `
        <!-- modal for repairorder -->
        <div class="modal fade" id="modal_cro_id_${
          fac.item_code
        }" tabindex="-1">
            ${this.modalForm(fac)}
        </div>
        <!-- end modal for repairder -->
        `;
    this.cardbody.innerHTML += card3;
    // end repairoder modal

    //add event for repair order save
    // this.AddEvent_RepairOrderSave(fac);
  };
}

class ListOfFacilities extends RowStyle {
  constructor(
    category,
    visible,
    cardbody,
    csrf_token,
    spinnerbox,
    maxdataAlert,
    foundItemAlert,
    searchbar
  ) {
    super(cardbody, csrf_token, spinnerbox, document);
    this.category = category;
    this.visible = visible;
    this.data = [];
    this.packages = [];
    this.no_of_items = 0;
    this.spinnerbox = spinnerbox;
    this.maxdataAlert = maxdataAlert;
    this.search = "";
    this.foundItemAlert = foundItemAlert;
    this.searchbar = searchbar;
    this.subItemHistory = [];
  }

  createRepairOrderModal = (fac) => {
    let modal = "";
    modal += `
                <div class="modal-dialog modal-dialog-scrollable">
                    <div class="modal-content">
                        <div class="modal-header">
                            <h5 class="modal-title">Create Repair Order</h5>
                            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>                        
                        </div>       
                        <div class="modal-body">
                            <!-- Floating Labels Form -->
                            <form class="row g-3" id="form-create-repairorder">
                                
                                <!-- HIDDEN DATA -->
                                <div class="col-md-12" style="display:none;">
                                    <div class="form-floating">        
                                        
                                        <input type="text" class="form-control" id="itemcodeid" placeholder="Item Code ID" value="${fac.random_item_code_id}" name="item_code_id">                         
                                        <label for="itemcodeid">Item Code ID</label>
                                    </div>
                                </div>
                                
                                <div class="col-md-12" style="display:none;">
                                    <div class="form-floating">        
                                        <input type="text" class="form-control" id="custodianid" placeholder="Custodian ID" value="${fac.custodian_id}" name="custodian_id">                         
                                        <label for="itemcodeid">Custodian ID</label>
                                    </div>
                                </div>
                    
                                <div class="col-md-12" style="display:none;">
                                    <div class="form-floating">        
                                        <input type="text" class="form-control" id="itemnamedescid" placeholder="Item Name Desc. ID" value="${fac.item_name_desc_id}" name="item_name_desc_id">                         
                                        <label for="itemcodeid">Item Name Description ID</label>
                                    </div>
                                </div>
                    
                                <div class="col-md-12">
                                    <div class="form-floating">
                                        
                                        <input type="text" class="form-control" id="floatingitemcode" placeholder="Item Code" value="${fac.item_code}" name="item_code">
                                        <label for="floatingitemcode">Item Code</label>
                                    </div>
                                </div>
                                <div class="col-md-12">
                                    <div class="form-floating">
                                        <input type="text" class="form-control" id="floatingitems" placeholder="Items" value="${fac.brand}" name="brand">
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

                                <div class="col-md-12">
                                    <div class="form-floating">
                                    <input type="text" class="form-control" id="floatingContactNumber" placeholder="Contact Number" name="contact_number">
                                    <label for="floatingContactNumber">Contact Number</label>
                                    </div>
                                </div>

                                <div class="col-md-12">
                                    <div class="alert alert-warning alert-dismissible fade show" role="alert" id="wowAlertID-${fac.random_item_code_id}" style="display:none;">    
                                    </div> 
                                </div>
                                              
                                <div class="modal-footer">
                                    <button type="button" class="btn btn-secondary" data-bs-dismiss="modal" id="dismissID">Close</button>
                                    <button type="submit" class="btn btn-primary">Save</button>
                                </div>   
                    
                            </form><!-- End floating Labels Form -->
                        </div>                       
                    </div> 
                </div>`;
    return modal;
  };

  async facility() {
    try {
      const response = await $.ajax({
        type: "GET",
        url: `/facilities_json/${this.category}/${this.visible}/${this.search}`,
      });

      console.log(this.search);

      this.data = response.fac_data;
      this.packages = response.packages;
      this.no_of_items = response.no_of_items;
    } catch (error) {
      console.log(error);
    }
  }

  async setNoOfItems() {
    this.foundItemAlert.style.display = "block";
    this.foundItemAlert.textContent = `${this.no_of_items} items has been found...`;
  }

  setVisible = (visible) => {
    this.visible = visible;
  };

  AddEventLoadMore(loadmoreBtn) {
    loadmoreBtn.addEventListener(
      "click",
      function (event) {
        event.preventDefault();
        this.visible += 5;
        this.fetchData(this.search);
      }.bind(this)
    );
  }

  async EventLoadMore() {
    const loadMoreBtn = document.getElementById("loadmoreid");
    this.AddEventLoadMore(loadMoreBtn);
  }

  async EventSaveRo() {
    this.data.forEach((fac) => {
      const formBtn = document.getElementById(
        `form-${fac.random_item_code_id}`
      );

      this.AddEventRepairOrderSave(formBtn, fac);
    });
  }

  async applyDesign() {
    let packages = this.packages;

    this.data.forEach((fac) => {
      this.design(fac, packages);
    });
  }

  async getSubItemsData(id) {
    try {
      const response = await $.ajax({
        type: "GET",
        url: `/subitem_history/${id}`,
        // url: `/under-repair-json1/`,
      });

      return response.subitemhistory;
    } catch (error) {
      console.log(error);
    }
  }

  subItemEvent = async () => {
    // add events
    let packages = this.packages;
    let getSubItemsData = this.getSubItemsData;

    this.data.forEach(function (fac) {
      packages.forEach(function (sub) {
        if (sub.item_code == fac.item_code) {
          const subItem = document.getElementById(`subitem_${sub.subitems_id}`);

          subItem?.addEventListener("click", function (e) {
            e.preventDefault();
            const s = getSubItemsData(`${sub.subitems_id}`);

            // dealing with a Promise object in JavaScript
            s.then((resolvedValue) => {
              const subItemModal = document.getElementById("SubItemListId");
              subItemModal.innerHTML = ``;

              resolvedValue.forEach((x) => {
                subItemModal.innerHTML += `
                                <a href="#" class="list-group-item list-group-item-action">
                                    <div class="d-flex w-100 justify-content-between">
                                        <h5 class="mb-1">${x.item_code}</h5>
                                        <small class="text-muted"></small>
                                    </div>
                                    <p class="mb-1">${x.item_name} - ${x.brand}</p>
                                    <small class="text-muted">Custodian: ${x.custodian}</small><br/>
                                    <small class="text-muted">${x.borrowed_to}: </small>
                                    <small class="text-muted">${x.borrowed_for}</small>
                                                                   
                                </a>
                                `;
              });
            }).catch((error) => {
              console.error(error); // Handle any errors that might occur during the Promise execution
            });
          });
        }
      });
    });
  };

  async applyEvents() {
    this.data.map((items, index) => {
      // const createRepairOrderBtn = document.getElementById("create");
      const createRepairOrderBtn = document.getElementById(
        `createRepairOrderBtn_${items.item_code}`
      );

      if (createRepairOrderBtn != null) {
        createRepairOrderBtn.addEventListener("click", function (event) {
          console.log("hello world!");
        });
      }
    });
  }

  async fetchData(search) {
    // search is from inputfield
    this.spinnerbox.style.display = "block";
    this.search = search;

    await this.facility();
    await this.setNoOfItems();
    await this.applyDesign();
    await this.PackageHistoryModal();
    await this.subItemEvent();
    await this.EventSaveRo();
    await this.applyEvents();

    setTimeout(() => {
      // display alert if hit the maximum size
      if (this.no_of_items <= this.visible) {
        this.maxdataAlert.style.display = "block";
      }

      // hide spinnerbox after loading data

      this.spinnerbox.style.display = "none";
    }, 1000);

    // Example usage: Scroll down by 500 pixels over 500 milliseconds
  }
}
// END CLASS FOR FACILITIES NEW
