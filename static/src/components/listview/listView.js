/** @odoo-module */

import { Component, useState, onWillUnmount } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";
import { rpc } from "@web/core/network/rpc";
import { FormView  } from "@app_onee/components/formView/formview";

export class ListViewAction extends Component {
    static template = "app_onee.listView";
    static components = {FormView };

    setup(){
       this.state = useState({
           'records':[],
           showCreateForm: false,
       });
//      this.orm=useService("orm");
       this.loadRecords();
       this.intervalId = setInterval(() => {this.loadRecords()},3000);
       this.onRecordCreated = this.onRecordCreated.bind(this);
       onWillUnmount(() => {clearInterval(this.intervalId)});

    }
//    async loadRecords(){
//       const result = await this.orm.searchRead('property',[],[]);
//       console.log(result);
//       this.state.records = result;
//    }

    async loadRecords(){
        const result = await rpc("/web/dataset/call_kw",{
            model: "property",
            method: "search_read",
            args:[[]],
            kwargs:{ fields: ['id','name','postcode','date_availability']}


        });
         console.log(result);
         this.state.records = result;

    };
    async createRecord(){
       await rpc("/web/dataset/call_kw",{
          model: "property",
          method: "create",
          args:[{
          name:"new property",
          postcode:"120120120",
          date_availability:"2025-04-24",
          }],
          kwargs:{},
       })

      this.loadRecords();

    };


    async deleteRecord(recordId){
        await rpc("/web/dataset/call_kw",{
           model:"property",
           method: "unlink",
           args:[recordId],
           kwargs:{}

          })

          this.loadRecords();

        };

    toggleCreateForm(){
       console.log("inside toggleCreateForm");
       this.state.showCreateForm = !this.state.showCreateForm;
       console.log(this.state.showCreateForm);
    };


    onRecordCreated(){
       this.loadRecords();
       this.state.showCreateForm = false;
    }



}

registry.category("actions").add(
    "app_onee.action_list_view",
    ListViewAction
);