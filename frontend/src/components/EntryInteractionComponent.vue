<template>
  <div>
    <div class="action-row">
      <b-field>
        <b-input
            v-model="newCalorieQuantity"
            type="number"
            placeholder="Enter calories"
        >
        </b-input>
        <b-button
            id="new-calorie-entry-button"
            icon-left="plus-circle"
            class="is-success is-outlined"
            @click="createEntry"
        >
          Create entry
        </b-button>
      </b-field>
    </div>
    <div class="action-row">
      <b-field>
      <b-input
          v-model="editEntryId"
          type="text"
          placeholder="Entry ID"
      >
      </b-input>
      <b-input
          v-model="editCalorieQuantity"
          type="number"
          placeholder="Updated calories"
          class="margin-left-1"
      >
      </b-input>
      <b-button
          id="edit-entry-button"
          icon-left="pencil"
          class="is-info is-outlined margin-left-1"
          @click="editEntry"
      >
        Edit entry
      </b-button>
    </b-field>
    </div>
    <div class="action-row">
      <b-field>
      <b-input
          v-model="deleteEntryId"
          type="text"
          placeholder="Entry ID"
      >
      </b-input>
      <b-button
          id="delete-entry-button"
          icon-left="delete"
          class="is-danger is-outlined margin-left-1"
          @click="deleteEntry"
      >
        Delete entry
      </b-button>
    </b-field>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

const urlBase = "http://127.0.0.1:8003";

export default {
  name: "EntryInteractionComponent",
  data() {
    return {
      newCalorieQuantity: null,
      editCalorieQuantity: null,
      editEntryId: null,
      deleteEntryId: null
    }
  },
  methods: {
    createEntry() {
      if (!this.newCalorieQuantity) {
        this.openDangerToast("You forgot to enter a calorie amount!");
        return;
      }
      const url = urlBase + "/calories/entry/create"
      axios.post(url, {
        "calories": parseInt(this.newCalorieQuantity)
      })
      .then( () => {
        this.openSuccessToast("Entry created successfully!");
        this.emitEntryUpdate();
      })
      .catch( (error) => {
        console.log(error);
      })
    },
    editEntry() {
      if (!this.editCalorieQuantity || !this.editEntryId) {
        this.openDangerToast("You forgot to enter a calorie amount or ID of document to edit!");
        return
      }

      const url = urlBase + "/calories/entry/edit";
      axios.post(url, {
        "document_id": this.editEntryId,
        "updatedDocument": {
          "calories": parseInt(this.editCalorieQuantity)
        }
      })
      .then( () => {
        this.openSuccessToast("Entry updated!");
        this.emitEntryUpdate();
      })
      .catch( () => {
        this.openDangerToast("Could not update document!");
      })
    },
    deleteEntry() {
      if (!this.deleteEntryId) {
        this.openDangerToast("You forgot to enter the ID of the document to delete!")
        return;
      }
      const url="http://127.0.0.1:8003/calories/entry/delete";
      axios.post(url, {
        document_id: this.deleteEntryId
      })
      .then( () => {
        this.openSuccessToast("Entry deleted successfully");
        this.emitEntryUpdate();
      })
      .catch( () => {
        this.openDangerToast("Could not delete document!")
      })
    },
    openDangerToast(message) {
      this.openToast(message, "is-danger");
    },
    openSuccessToast(message) {
      this.openToast(message, "is-success");
    },
    openToast(message, type) {
      this.$buefy.toast.open({
        message: message,
        type: type,
        position: "is-top-right"
      })
    },
    emitEntryUpdate() {
      console.log("Emitting!");
      this.$emit("entry-update");
    }
  }
}
</script>

<style scoped lang="scss">

  .action-row {
    @include bordered-dashboard-card;
    margin-bottom: 1rem;
    padding: 2rem;
  }

  #new-calorie-entry-button {
    margin-left: 1rem;
  }

</style>
