<script setup lang="ts"> 
import IconUser from '~icons/custom/user'
import IconKeyboard from '~icons/custom/keyboard'
import IconCheck from '~icons/custom/check'
import IconEmail from '~icons/custom/email'

const props = defineProps({
    visible: Boolean
})
const visible = ref(props.visible)
const emit = defineEmits(['closeLogin'])
type LoginData = {
  name: string,
  pass: string
}

type RegisterData = {
  name: string,
  pass: string,
  checkPass: string,
  email: string,
  checkCode: string
}
const loginData = reactive<LoginData>({
  name: '',
  pass: ''
})
const registerData = reactive<RegisterData>({
  name: "",
  pass: "",
  checkPass: "",
  email: "",
  checkCode: ""
})

const closeDialog = () => {
  emit('closeLogin')
}

watch(() => props.visible, (value: boolean) => {
  if(value === true) {
    visible.value = true
  }
})

</script>

<template>
  <el-dialog class="login" v-model="visible" @close="closeDialog">
    <el-card class="form-container">
      <el-tabs >
          <el-tab-pane label="login" >
            <template #label>
              <span class="custom-tabs-label">  
                密码登录 
              </span>
            </template>
            <el-form :model="loginData">
              <el-form-item>
                <el-input v-model="loginData.name"  placeholder="用户名">
                  <template #prefix>
                    <el-icon class="form-icon"> <IconUser/></el-icon>
                  </template>
                </el-input>
              </el-form-item>
              <el-form-item>
                <el-input v-model="loginData.pass" type="password" placeholder="请输入密码">
                  <template #prefix>
                    <el-icon class="form-icon"><IconKeyboard /></el-icon>
                  </template>
                </el-input>
              </el-form-item>
            </el-form>
          </el-tab-pane> 
          <el-tab-pane label="register" >
            <template #label>
              <span class="custom-tabs-label">  
                用户注册
              </span>
            </template>
            <el-form :model="registerData">
              <el-form-item>
                <el-input v-model="registerData.name"  placeholder="用户名">
                  <template #prefix>
                    <el-icon class="form-icon"> <IconUser/></el-icon>
                  </template>
                </el-input>
              </el-form-item>
              <el-form-item>
                <el-input v-model="registerData.pass" type="password" placeholder="请输入密码">
                  <template #prefix>
                    <el-icon class="form-icon"><IconKeyboard /></el-icon>
                  </template>
                </el-input>
              </el-form-item>
              <el-form-item>
                <el-input v-model="registerData.checkPass" type="password" placeholder="请再次输入密码">
                  <template #prefix>
                    <el-icon class="form-icon"><IconKeyboard /></el-icon>
                  </template>
                </el-input>
              </el-form-item>
              <el-form-item>
                <el-input v-model="registerData.email"  placeholder="请输入邮箱">
                  <template #prefix>
                    <el-icon class="form-icon"><IconEmail /></el-icon>
                  </template>
                  <template #suffix>
                    <el-button class='base-button check-button'>验证</el-button>
                  </template>
                </el-input>
              </el-form-item>
              <el-form-item>
                <el-input v-model="registerData.checkCode" placeholder="请输入邮箱验证码">
                  <template #prefix>
                    <el-icon class="form-icon"><IconCheck /></el-icon>
                  </template>
                </el-input>
              </el-form-item>
            </el-form> 
          </el-tab-pane>
      </el-tabs>
    </el-card>
  </el-dialog>
</template>

<style lang="less"> 
@import '@/styles/variables.less';
.el-dialog.login {
    // background: #AEBDDB;
    background-image: url('../assets/background3.png');
    background-size: cover;
    border-radius: 15px;
    max-width: 600px;
    height: 50% ;
    width: 50% ;
    .el-dialog__headerbtn:hover .el-dialog__close {
      color:  #fff;
    }

    .el-dialog__headerbtn:focus .el-dialog__close {
      color:  #fff;
    }
    .el-dialog__close {
      color: @theme-color;
 
    }

    .form-container {
        border-radius: 15px;
        margin-top: 20px;
        margin: 20px;
        .form-icon {
          color: #777;
          font-size: 20px;
        }

        .el-input {
          height: 45px;
        }
        .el-input__wrapper.is-focus {
          box-shadow: 0 0 0 1px  #7697da inset;
        }
    }

    .el-tabs__active-bar {
      background-color: #AEBDDB;
    }

    .custom-tabs-label {
      font-size: 18px;
      font-weight: bold;
      color: #888;
      margin: 0 20px; 
      &:hover {
        color:@theme-color;
      }
    }

    .el-tabs__header {
      margin: 0 0 20px;
    }

    .el-tabs__item {
      padding: 0px;
    }

    .el-tabs__item.is-active {
      .custom-tabs-label {
        color:@theme-color;
      }

    }

    .el-tabs__nav-wrap {
      height: 50px;
      width: 100%;
    }
    .el-tabs__nav {
      height: 50px;
    }

    .check-button {
      font-size: 12px;

    }
    
}
</style>
