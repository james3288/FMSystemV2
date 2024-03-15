class RepairOrder {
  constructor(category, item_code, visible, search, cardbody) {
    this.category = category;
    this.item_code = item_code;
    this.visible = visible;
    this.search = search;
    this.data = [];
    this.cardbody = cardbody;
    this.rep_released_id = 0;
    this.repair_order_id = 0;

    // temporary storage
  }

  // row design
  row = (value, col_name) => {
    let aa = ``;
    aa += `
        <div class="card-title p-1 fs-6 text-white badge bg-info mx-0 my-1">
            <i class="bi bi-grip-vertical"></i> ${col_name} <i class="bi bi-grip-vertical"></i>
        </div>
        <div class="card-text m-0">
            <ul class="list-group">          
                <li class="list-group-item p-1">
                    <i class="bi bi-gear"></i> 
                    <span class="card-title" style="font-size:14px !important;">
                      ${
                        col_name === "Status"
                          ? value === "Repaired"
                            ? `<span style="background-color:green; color: white;padding:3px 5px; border-radius:5px;">${value}</span>`
                            : `<span style="background-color:red; color: white;padding:3px 5px; border-radius:5px;">${value}</span>`
                          : value
                      }
                    </span>                      
                </li>                                         
            </ul>
        </div>
        `;

    return aa;
  };
  // end row design

  // repairorder na column | left side
  repairOrder_row = (repair) => {
    let bb = ``;

    bb += this.row(repair.custodian_name, "Custodian Name");
    bb += this.row(repair.repair_order_no, "Repair Order No");
    bb += this.row(repair.problem_encountered, "Problem Encountered");
    bb += this.row(repair.delivered_by, "Delivered By");
    bb += this.row(repair.received_by, "Received By");
    bb += this.row(repair.delivered_date, "Date Delivered");
    bb += this.row(repair.contact_no, "Contact No");

    return bb;
  };
  // end repair order na column

  // repair turnoder na column | right side
  repairTurnover_row = (repair) => {
    let bb = ``;
    let turnover_data = this.data.turnover_data;
    let count = 0;

    turnover_data.forEach(
      function (x) {
        if (repair.repair_order_id === x.repair_order_id) {
          bb += this.row(x.details_work_done, "Details Work Done");
          bb += this.row(x.released_to, "Released To");
          bb += this.row(x.repaired_by, "Repaired By");
          bb += this.row(x.status, "Status");
          bb += this.row(x.released_date, "Date Released");
          bb += this.row(x.date_repaired, "Date Repaired");
          count += 1;
        }
      }.bind(this)
    );

    if (count === 0) {
      bb += `
            <div class="alert alert-danger alert-dismissible fade show" role="alert">
                Repair On-going!
            </div>
            `;
    }

    return bb;
  };
  // End rapair turnover na column

  removeTurnoverEvent = (id) => {
    fetch(`/repair_turnover_delete/${id}`, {
      method: "POST",
      headers: {
        "X-CSRFToken": getCSRFToken(), // Include CSRF token for security (see step 3)
      },
    })
      .then(function (response) {
        // Process the response from the Django view if needed

        location.reload(true);
        // var repairpage_url = '/under-repair/under-repair-items/' + fac.item_code;
        // window.location.href = repairpage_url;
      })
      .catch(function (error) {
        console.log("Error:", error);
      });
  };

  removeRepairOrderEvent = (id) => {
    fetch(`/repair_order_delete/${id}`, {
      method: "POST",
      headers: {
        "X-CSRFToken": getCSRFToken(), // Include CSRF token for security (see step 3)
      },
    })
      .then(function (response) {
        // Process the response from the Django view if needed

        location.reload(true);

        // var repairpage_url = '/under-repair/under-repair-items/' + fac.item_code;
        // window.location.href = repairpage_url;
      })
      .catch(function (error) {
        console.log("Error:", error);
      });
  };

  addEditTurnoverSaveEvent = (id, form, option) => {
    let turnoverAlert = document.getElementById("turnoverAlertId");
    turnoverAlert.style.display = "none !important";

    // check if some textfield are empty
    var inputFields = document.querySelectorAll(`#form-addTurnover input`);

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
      turnoverAlert.textContent = "Some input fields are empty.";
      turnoverAlert.style.display = "block";
    } else {
      // var wowAlert1 = document.getElementById(`wowAlertID-${fac.random_item_code_id}`);
      console.log("All input fields are filled.");
      // wowAlert1.style.display = 'none';

      const formData = new FormData(form);
      formData.append("id", id);
      formData.append("option", option);

      fetch("/repair_turnover/", {
        method: "POST",
        headers: {
          "X-CSRFToken": getCSRFToken(), // Include CSRF token for security (see step 3)
        },
        body: formData,
      })
        .then(function (response) {
          // Process the response from the Django view if needed

          location.reload(true);
          // var repairpage_url = '/under-repair/under-repair-items/' + fac.item_code;
          // window.location.href = repairpage_url;
        })
        .catch(function (error) {
          console.log("Error:", error);
        });
    }
  };

  editRepairOrderEvent = (id, form, option) => {
    let repairOrderAlert = document.getElementById("repairOrderAlertId");
    repairOrderAlert.style.display = "none !important";

    // check if some textfield are empty
    var inputFields = document.querySelectorAll(`#form-editRepairOrder input`);

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
      turnoverAlert.textContent = "Some input fields are empty.";
      turnoverAlert.style.display = "block";
    } else {
      // var wowAlert1 = document.getElementById(`wowAlertID-${fac.random_item_code_id}`);
      console.log("All input fields are filled.");
      // wowAlert1.style.display = 'none';

      const formData = new FormData(form);
      formData.append("id", id);
      formData.append("option", option);

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
          // var repairpage_url = '/under-repair/under-repair-items/' + fac.item_code;
          // window.location.href = repairpage_url;
        })
        .catch(function (error) {
          console.log("Error:", error);
        });
    }
  };

  // load Turnover data for edit
  loadTurnoverDataToModal = (repair_order_id) => {
    let turnover_data = this.data.turnover_data;

    turnover_data.forEach(
      function (xx) {
        if (xx.repair_order_id === repair_order_id) {
          const detailsWorkDone = document.getElementById(
            "floatDetailsWorkDone"
          );
          const releasedTo = document.getElementById("floatingReleasedTo");
          const repairedBy = document.getElementById("floatingRepairedBy");
          const status = document.getElementById("floatingStatus");
          const dateReleased = document.getElementById("floatingTurnoverDate");
          const dateRepaired = document.getElementById("floatingRepairedDate");
          const btnUpdate = document.getElementById("floatingBtnTurnover");

          this.rep_released_id = xx.rep_released_id;
          detailsWorkDone.value = xx.details_work_done;
          releasedTo.value = xx.released_to;
          repairedBy.value = xx.repaired_by;
          status.value = xx.status;
          var dateTurnoverToSet = new Date(xx.released_date);
          dateTurnoverToSet.setDate(dateTurnoverToSet.getDate() + 1);

          var dateRepairedToSet = new Date(xx.date_repaired);
          dateRepairedToSet.setDate(dateRepairedToSet.getDate() + 1);

          // Format the date as "YYYY-MM-DD"
          dateReleased.value = dateTurnoverToSet.toISOString().slice(0, 10);
          dateRepaired.value = dateRepairedToSet.toISOString().slice(0, 10);
          btnUpdate.textContent = "Update";

          // console.log(this.rep_released_id)
        }
      }.bind(this)
    );

    // detailsWorkDone.value = x.detailsWorkDone
  };
  // end load turnover data for edit

  loadRepairOrderDataToModal = (repair_order_id) => {
    let repairOrder_data = this.data.repair_order_data;

    repairOrder_data.forEach(
      function (xx) {
        if (xx.repair_order_id === repair_order_id) {
          const itemCode = document.getElementById("floatingitemcode");
          const problemEncountered = document.getElementById("floatingProblem");
          const deliveredBy = document.getElementById("floatingDeliveredBy");
          const receivedBy = document.getElementById("floatingReceivedBy");
          const dateDelivered = document.getElementById("floatingDate");
          const contactNumber = document.getElementById(
            "floatingContactNumber"
          );

          itemCode.value = xx.item_code;
          problemEncountered.value = xx.problem_encountered;
          deliveredBy.value = xx.delivered_by;
          receivedBy.value = xx.received_by;
          contactNumber.value = xx.contact_no;

          var dateDeliveredSet = new Date(xx.delivered_date);
          dateDeliveredSet.setDate(dateDeliveredSet.getDate() + 1);
          dateDelivered.value = dateDeliveredSet.toISOString().slice(0, 10);
        }
      }.bind(this)
    );
  };

  // Turnover Event
  async addTurnoverEvent() {
    // get add button id
    let repair_order_data = this.data.repair_order_data;
    let rep_released_id = this.rep_released_id;
    let repair_order_id = this.repair_order_id;

    repair_order_data.forEach(
      function (x) {
        const addTurnoverBtn = document.getElementById(
          `addTurnover_${x.repair_order_id}`
        );
        const updateTurnoverBtn = document.getElementById(
          `updateTurnover_${x.repair_order_id}`
        );
        const updateRepairOrderBtn = document.getElementById(
          `updateRepairOrder_${x.repair_order_id}`
        );
        const removeTurnoverBtn = document.getElementById(
          `removeTurnover_${x.repair_order_id}`
        );
        const removeRepairOrderBtn = document.getElementById(
          `removeRepairOrder_${x.repair_order_id}`
        );

        const turnoverSaveUpdateEvent = this.addEditTurnoverSaveEvent;
        const editRepairOrderEvent = this.editRepairOrderEvent;
        const turnoverDataToModal = this.loadTurnoverDataToModal;
        const repairOrderDataToModal = this.loadRepairOrderDataToModal;
        const removeTurnoverEvent = this.removeTurnoverEvent;
        const removeRepairOrderEvent = this.removeRepairOrderEvent;

        // ADD BUTTON
        if (addTurnoverBtn != null) {
          // FOR ADD TURNOVER BUTTON EVENT
          addTurnoverBtn.addEventListener("click", function (event) {
            var btnForm = document.getElementById("form-addTurnover");

            btnForm.addEventListener("submit", function (e) {
              e.preventDefault();
              turnoverSaveUpdateEvent(x.repair_order_id, btnForm, "save");
            });
          });
        }

        // UPDATE BUTTON FOR REPAIRORDER
        if (updateRepairOrderBtn != null) {
          // FOR UPDATE TURNOVER BUTTON EVENT
          updateRepairOrderBtn.addEventListener("click", function (event) {
            var btnForm = document.getElementById("form-editRepairOrder");
            repairOrderDataToModal(x.repair_order_id);

            btnForm.addEventListener("submit", function (e) {
              e.preventDefault();
              editRepairOrderEvent(x.repair_order_id, btnForm, "update");
            });
          });
        }

        // UPDATE BUTTON FOR TURNOVER
        if (updateTurnoverBtn != null) {
          // FOR UPDATE TURNOVER BUTTON EVENT
          updateTurnoverBtn.addEventListener("click", function (event) {
            var btnForm = document.getElementById("form-addTurnover");
            turnoverDataToModal(x.repair_order_id);

            btnForm.addEventListener("submit", function (e) {
              e.preventDefault();
              turnoverSaveUpdateEvent(rep_released_id, btnForm, "update");
            });
          });
        }

        // REMOVE BUTTON
        if (removeTurnoverBtn != null) {
          // FOR REMOVE TURNOVER BUTTON EVENT
          removeTurnoverBtn.addEventListener("click", function (event) {
            var btnForm = document.getElementById("form-removeTurnover");

            btnForm.addEventListener("submit", function (e) {
              e.preventDefault();

              removeTurnoverEvent(rep_released_id);
            });
          });
        }

        // REMOVE BUTTON
        if (removeRepairOrderBtn != null) {
          // FOR REMOVE REPAIRORDER BUTTON EVENT
          removeRepairOrderBtn.addEventListener("click", function (event) {
            var btnForm = document.getElementById("form-removeRepairOrder");

            btnForm.addEventListener("submit", function (e) {
              e.preventDefault();

              removeRepairOrderEvent(x.repair_order_id);
            });
          });
        }
      }.bind(this)
    );
  }
  // End Turnover Event

  // Modal for AddTurnover
  async TurnoverModal() {
    let cc = `
        <div class="modal fade" id="AddTurnoverModal" tabindex="-1" style="display: none;" aria-hidden="true">
            <div class="modal-dialog">
                <div class="modal-content">
                    <div class="modal-header">
                        <form class="row g-3" id="form-addTurnover">
                            <div class="col-md-12">
                                <div class="form-floating"> 
                                    <input type="text" class="form-control" id="floatDetailsWorkDone" placeholder="Details Work Done" value="" name="details_work_done">            
                                    <label for="floatDetailsWorkDone">Details Work Done</label>
                                </div>
                            </div>

                            <div class="col-md-12">
                                <div class="form-floating">
                                    <input type="text" class="form-control" id="floatingReleasedTo" placeholder="Released To" name="released_to">
                                    <label for="floatingReleasedTo">Released To</label>
                                </div>
                            </div>

                            <div class="col-md-12">
                                <div class="form-floating">
                                    <input type="text" class="form-control" id="floatingRepairedBy" placeholder="Repaired By" name="repaired_by">
                                    <label for="floatingRepairedBy">Repaired By</label>
                                </div>
                            </div>

                            <div class="col-md-12">
                                <div class="form-floating">
                                    <select class="form-select" aria-label="Default select example" id="floatingStatus" placeholder="Repaired By" name="status">
                                        <option value="" selected disabled>Status</option>
                                        <option value="Repaired">Repaired</option>
                                        <option value="Defective">Defective</option>
                                    </select>
                                </div>
                            </div>

                            <div class="col-md-12">
                                <div class="form-floating">
                                    <input type="date" class="form-control" id="floatingTurnoverDate" name="turnover_date">
                                    <label for="floatingTurnoverDate">Date Released</label>
                                </div>
                            </div>

                            <div class="col-md-12">
                                <div class="form-floating">
                                    <input type="date" class="form-control" id="floatingRepairedDate" name="repaired_date">
                                    <label for="floatingRepairedDate">Date Repaired</label>
                                </div>
                            </div>

                            <div class="text-center"></div>
                            <div class="col-md-12">
                                <div class="alert alert-warning alert-dismissible fade show" role="alert" id="turnoverAlertId" style="display:none;">    
                                </div> 
                            </div>
                            <div class="modal-footer">
                                <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                                <button type="submit" class="btn btn-primary" id="floatingBtnTurnover">Save</button>
                            </div>

                        </form>
                    </div>
                </div>
            </div>
        </div>
        `;
    this.cardbody.innerHTML += cc;
  }

  async EditRepairOrderModal() {
    let cc = `
        <div class="modal fade" id="EditRepairOrderModal" tabindex="-1" style="display: none;" aria-hidden="true">
            <div class="modal-dialog">
                <div class="modal-content">
                    <div class="modal-header">
                        <form class="row g-3" id="form-editRepairOrder">
      
                            <div class="col-md-12">
                                <div class="form-floating">                       
                                    <input type="text" class="form-control" id="floatingitemcode" placeholder="Item Code" name="item_code">
                                    <label for="floatingitemcode">Item Code</label>
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
                                <div class="alert alert-warning alert-dismissible fade show" role="alert" id="" style="display:none;">    
                                </div> 
                            </div>

                            <div class="col-md-12">
                                <div class="alert alert-warning alert-dismissible fade show" role="alert" id="repairOrderAlertId" style="display:none;">    
                                </div> 
                            </div>
                                            
                            <div class="modal-footer">
                                <button type="button" class="btn btn-secondary" data-bs-dismiss="modal" id="dismissID">Close</button>
                                <button type="submit" class="btn btn-primary">Update</button>
                            </div>   
                        </form>
                    </div>
                </div>
            </div>
        </div>
        `;

    this.cardbody.innerHTML += cc;
  }

  async removeModal() {
    let cc = `
        <div class="modal fade" id="basicModal" tabindex="-1">
            <div class="modal-dialog">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title">FMS INFO:</h5>
                        <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                    </div>
                    <form class="row g-3 px-3" id="form-removeTurnover">
                        <div class="modal-body">
                            <span class="delete-message">Are you sure you want to remove repair turnover info?</span>
                        </div>
                        <div class="modal-footer">
                            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">No</button>
                            <button type="submit" class="btn btn-danger">Yes</button>
                        </div>
                    </form>
                    
                </div>
            </div>
        </div>
        `;
    this.cardbody.innerHTML += cc;
  }

  async removeModal_() {
    let cc = `
        <div class="modal fade" id="basicModal1" tabindex="-1">
            <div class="modal-dialog">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title">FMS INFO:</h5>
                        <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                    </div>
                    <form class="row g-3 px-3" id="form-removeRepairOrder">
                        <div class="modal-body">
                            <span class="delete-message">Are you sure you want to remove repair order info?</span>
                        </div>
                        <div class="modal-footer">
                            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">No</button>
                            <button type="submit" class="btn btn-danger">Yes</button>
                        </div>
                    </form>             
                </div>
            </div>
        </div>
        `;
    this.cardbody.innerHTML += cc;
  }

  // End Modal for AddTurnover

  async applyDesign() {
    let repair_data = this.data.repair_order_data;
    let turnover_data = this.data.turnover_data;
    let rep_released_id = 0;

    // using this method, you can check if either already turnover or not
    var count = (repair_order_id) => {
      var i = 0;

      turnover_data.forEach(
        function (xx) {
          if (repair_order_id == xx.repair_order_id) {
            this.rep_released_id = xx.rep_released_id;
            i += 1;
          }
        }.bind(this)
      );
      return i;
    };

    // BUTTONS HERE
    let addBtnRo = (x, repair_order_id) => {
      var wow = ``;

      if (x == 1) {
        wow = ``;
      } else if (x == 2) {
        if (count(repair_order_id) == 0) {
          wow = `<a class="btn btn-light" style="color:white !important; padding:1px !important; margin:-3px !important;" id="addTurnover_${repair_order_id}" data-bs-toggle="modal" data-bs-target="#AddTurnoverModal"><i class="bi bi-plus-circle-fill" style="color:#004852 !important;"></i></a>`;
        } else {
          wow = ``;
        }
      }
      return wow;
    };

    let updateBtnRo = (x, repair_order_id) => {
      var wow = ``;

      if (x == 1) {
        wow = `<a class="btn btn-light" style="color:white !important; padding:1px !important; margin:-3px !important;" id="updateRepairOrder_${repair_order_id}" data-bs-toggle="modal" data-bs-target="#EditRepairOrderModal"><i class="bi bi-pencil-fill" style="color:#2C9DA5 !important;"></i></a>`;
      } else if (x == 2) {
        if (count(repair_order_id) == 0) {
          wow = ``;
        } else {
          wow = `<a class="btn btn-light" style="color:white !important; padding:1px !important; margin:-3px !important;" id="updateTurnover_${repair_order_id}" data-bs-toggle="modal" data-bs-target="#AddTurnoverModal"><i class="bi bi-pencil-fill" style="color:#2C9DA5 !important;"></i></a>`;
        }
      }
      return wow;
    };

    let removeBtnRo = (x, repair_order_id) => {
      var wow = ``;
      if (x == 1) {
        wow = `<a class="btn btn-light" style="color:white !important; padding:1px !important; margin:-3px !important;" id="removeRepairOrder_${repair_order_id}" data-bs-toggle="modal" data-bs-target="#basicModal1"><i class="bi bi-x-circle-fill" style="color:#004852 !important;"></i></a>`;
      } else if (x == 2) {
        if (count(repair_order_id) == 0) {
          wow = ``;
        } else {
          wow = `<a class="btn btn-light" style="color:white !important; padding:1px !important; margin:-3px !important;" id="removeTurnover_${repair_order_id}" data-bs-toggle="modal" data-bs-target="#basicModal"><i class="bi bi-x-circle-fill" style="color:#004852 !important;"></i></a>`;
        }
      }
      return wow;
    };
    // END BUTTONS HERE

    repair_data.forEach((x) => {
      let aa = ``;
      aa += `
            <div class="card-body" id="fac_id">    
                <div class="container-fluid">
                    <div class="row">
                        <div class="col-lg-6 p-2">
                            <div class="card" style="margin-bottom:20px !important;" id="top_right_id">                 
                                <div class="card-header bg-light fs-4">
                                    <div class="float-left">
                                        REPAIR ORDER INFO:
                                    </div>

                                   <!-- Update/Delete for Repair Order -->
                                    <div class="float-end">
                                        ${updateBtnRo(1, x.repair_order_id)}
                                        ${removeBtnRo(1, x.repair_order_id)}
                                    </div>
                                    <!-- End Update/Delete for Repair Order -->
                                   
                                </div>
                                <div class="card-body">            
                                    <div class="card-title p-1 m-0">${
                                      x.item_code
                                    }</div>
                                    ${this.repairOrder_row(x)}
                                </div>
                            </div>                          
                        </div>

                        <div class="col-lg-6 p-2">
                            <div class="card" style="margin-bottom:20px !important;" id="top_right_id">                 
                                <div class="card-header bg-light fs-4">
                                    <div class="float-left">
                                        REPAIR TURNOVER INFO
                                    </div>
                                    
                                    <!-- Add/Update/Delete for Repair Order Turnover -->
                                    <div class="float-end">
                                        
                                        ${addBtnRo(2, x.repair_order_id)}
                                        ${updateBtnRo(2, x.repair_order_id)}
                                        ${removeBtnRo(2, x.repair_order_id)}
                                        </div>    
                                    <!-- End Add/Update/Delete for Repair Order Turnover -->
                                </div>
                                <div class="card-body">            
                                    <div class="card-title p-1 m-0">${
                                      x.item_code
                                    }</div>
                                        ${this.repairTurnover_row(x)}
                                    </div>
                                </div>                              
                            </div> 
                        </div>              
                </div>

            </div>
            `;

      this.cardbody.innerHTML += aa;
    });
  }

  async getRepairOrder() {
    try {
      const response = await $.ajax({
        type: "GET",
        url: `/under-repair-json/${this.category}/${this.visible}/${this.item_code}/${this.search}`,
        // url: `/under-repair-json1/`,
      });

      this.data = response;
    } catch (error) {
      console.log(error);
    }
  }

  async fetchData(search) {
    await this.getRepairOrder(); // get data from database
    await this.applyDesign(); // apply ui
    await this.TurnoverModal(); // add Turnover modals
    await this.EditRepairOrderModal(); // add Edit modals
    await this.removeModal(); // add remove modals
    await this.removeModal_(); // add remove modals for repairorder
    await this.addTurnoverEvent(); // add events
  }
}
