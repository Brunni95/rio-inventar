<script setup>
const props = defineProps({ id: { type: Number, required: true }, number: { type: String, required: true } });
const qrUrl = `/api/v1/assets/${props.id}/qrcode`;
const download = async () => {
  const a = document.createElement('a');
  a.href = qrUrl;
  a.download = `qr-${props.number || props.id}.png`;
  document.body.appendChild(a);
  a.click();
  a.remove();
};
</script>

<template>
  <button class="btn" @click="download" title="QR-Code herunterladen">QR</button>
</template>

<style scoped>
.btn { border: 1px solid var(--color-border); background: var(--btn-bg); color: var(--text-strong); border-radius: 6px; padding: 0.3rem 0.5rem; }
</style>


