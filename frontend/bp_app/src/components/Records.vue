<template>
    <div>
        <h1>Records</h1>
        <div v-bind:key="record.id" v-for="record in records">
            <h3>{{ record.notes }}</h3>
        </div>
    </div>
</template>

<script>
export default {
    name: "Records",
    props: ["records"]
}
</script>

<style scoped>

</style>