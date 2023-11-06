<template>
  <div
    style="
      width: 300px;
      height: 380px;
      border: none;
      border-radius: 12px;
      background-color: #252632;
      position: relative;
    "
  >
    <div
      style="
        position: absolute;
        top: 0;
        left: 0;
        background-color: rgb(57 60 97 / 64%);
        border-radius: 12px;
        z-index: 100;
        width: 100%;
        height: 100%;
      "
    ></div>
    <div style="position: absolute; top: 0; left: 0">
      <el-skeleton-item
        variant="image"
        style="
          width: 300px;
          height: 300px;
          margin: auto;
          border-top-right-radius: 12px;
          border-top-left-radius: 12px;
        "
      />
      <div style="padding: 14px">
        <el-skeleton-item variant="p" style="width: 50%" />
        <div style="display: flex; align-items: center; justify-items: space-between">
          <el-skeleton-item variant="text" style="margin-right: 16px" />
          <el-skeleton-item variant="text" style="width: 30%" />
        </div>
      </div>
    </div>
  </div>
</template>
