<script setup lang="ts">
  import IconUser from '~icons/custom/user'
  import IconKeyboard from '~icons/custom/keyboard'
  import IconCheck from '~icons/custom/check'
  import IconEmail from '~icons/custom/email'
  import type { FormInstance } from 'element-plus'
  import { ElMessage } from 'element-plus'

  const props = defineProps({
    visible: Boolean,
  })
  const visible = ref(props.visible)
  const emit = defineEmits(['closeLogin'])
  type LoginData = {
    name: string
    pass: string
  }

  type RegisterData = {
    name: string
    pass: string
    checkPass: string
    email: string
    checkCode: string
  }
  const loginData = reactive<LoginData>({
    name: '',
    pass: '',
  })
  const registerData = reactive<RegisterData>({
    name: '',
    pass: '',
    checkPass: '',
    email: '',
    checkCode: '',
  })

  const loginFormRef = ref<InstanceType<typeof FormInstance>>()
  const registerFormRef = ref<InstanceType<typeof FormInstance>>()

  const closeDialog = () => {
    emit('closeLogin')
  }

  const loginRules = {
    name: [{ required: true, message: '请输入用户名', trigger: 'blur' }],
    pass: [{ required: true, message: '密码不得为空', trigger: 'blur' }],
  }

  const validatePass = (rule: any, value: any, callback: any) => {
    const reg = /^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)[A-Za-z\d!#$%^&*?]{6,16}$/
    const reg2 = /[A-Za-z\d!#$%^&*?]{6,16}$/
    if (value === '') {
      callback(new Error('密码不得为空'))
    } else if (value.length < 6 || value.length > 16) {
      callback(new Error('密码长度应为6-16之间'))
    } else if (!reg2.test(value)) {
      callback(new Error('密码仅允许特殊字符!#$%^&*?'))
    } else if (!reg.test(value)) {
      callback(new Error('密码至少包含1个大写字母、1个小写字母和1个数字'))
    } else {
      callback()
    }
  }

  const validateCheckPass = (rule: any, value: any, callback: any) => {
    if (value === '') {
      callback(new Error('请再次输入密码'))
    } else if (value !== registerData.pass) {
      callback(new Error('密码输入不一致!'))
    } else {
      callback()
    }
  }

  const registerRules = {
    name: [{ required: true, message: '请输入用户名', trigger: 'blur' }],
    pass: [{ validator: validatePass, trigger: ['blur', 'change'] }],
    checkPass: [{ validator: validateCheckPass, trigger: ['blur', 'change'] }],
    email: [
      { required: true, message: '请输入邮箱', trigger: 'blur' },
      { type: 'email', message: '请输入正确的邮箱格式', trigger: ['change', 'blur'] },
    ],
    checkCode: [{ required: true, message: '验证码不得为空', trigger: 'blur' }],
  }

  const handleRegister = (formEL: InstanceType<typeof FormInstance>) => {
    if (!formEL) return
    formEL.validate((valid: boolean) => {
      if (valid) {
      } else {
        ElMessage({
          message: '请确认信息输入无误',
          type: 'error',
        })
        return false
      }
    })
    ElMessage({
      message: '注册成功',
      type: 'success',
    })
  }

  const handleLogin = (formEL: InstanceType<typeof FormInstance>) => {
    if (!formEL) return
    formEL.validate((valid: boolean) => {
      if (valid) {
      } else {
        ElMessage({
          message: '请确认信息输入无误',
          type: 'error',
        })
        return false
      }
    })
    ElMessage({
      message: '登录成功',
      type: 'success',
    })
  }

  watch(
    () => props.visible,
    (value: boolean) => {
      if (value === true) {
        visible.value = true
      }
    },
  )
</script>

<template>
  <el-dialog class="login" v-model="visible" @close="closeDialog">
    <el-card class="form-container">
      <el-tabs>
        <!-- 登录 -->
        <el-tab-pane label="login">
          <template #label>
            <span class="custom-tabs-label"> 密码登录 </span>
          </template>
          <el-form :model="loginData" :rules="loginRules" ref="loginFormRef" status-icon>
            <el-form-item class="login-form-item" prop="name">
              <el-input v-model="loginData.name" placeholder="用户名">
                <template #prefix>
                  <el-icon class="form-icon"> <IconUser /></el-icon>
                </template>
              </el-input>
            </el-form-item>
            <el-form-item class="login-form-item" prop="pass">
              <el-input v-model="loginData.pass" type="password" placeholder="请输入密码">
                <template #prefix>
                  <el-icon class="form-icon"><IconKeyboard /></el-icon>
                </template>
              </el-input>
            </el-form-item>
          </el-form>
          <el-button class="base-button bottom-button" @click="handleLogin(loginFormRef)"
            >登录</el-button
          >
        </el-tab-pane>
        <!-- 注册 -->
        <el-tab-pane label="register">
          <template #label>
            <span class="custom-tabs-label"> 用户注册 </span>
          </template>
          <el-form :model="registerData" :rules="registerRules" ref="registerFormRef" status-icon>
            <el-form-item class="login-form-item" prop="name">
              <el-input v-model="registerData.name" placeholder="用户名">
                <template #prefix>
                  <el-icon class="form-icon"> <IconUser /></el-icon>
                </template>
              </el-input>
            </el-form-item>
            <el-form-item class="login-form-item" prop="pass">
              <el-input v-model="registerData.pass" type="password" placeholder="请输入密码">
                <template #prefix>
                  <el-icon class="form-icon"><IconKeyboard /></el-icon>
                </template>
              </el-input>
            </el-form-item>
            <el-form-item class="login-form-item" prop="checkPass">
              <el-input
                v-model="registerData.checkPass"
                type="password"
                placeholder="请再次输入密码"
              >
                <template #prefix>
                  <el-icon class="form-icon"><IconKeyboard /></el-icon>
                </template>
              </el-input>
            </el-form-item>
            <el-form-item class="login-form-item" prop="email">
              <el-input v-model="registerData.email" placeholder="请输入邮箱">
                <template #prefix>
                  <el-icon class="form-icon"><IconEmail /></el-icon>
                </template>
                <template #suffix>
                  <el-button class="base-button check-button">验证</el-button>
                </template>
              </el-input>
            </el-form-item>
            <el-form-item class="login-form-item" prop="checkCode">
              <el-input v-model="registerData.checkCode" placeholder="请输入邮箱验证码">
                <template #prefix>
                  <el-icon class="form-icon"><IconCheck /></el-icon>
                </template>
              </el-input>
            </el-form-item>
          </el-form>
          <el-button class="base-button bottom-button" @click="handleRegister(registerFormRef)"
            >注册</el-button
          >
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
    height: 50%;
    width: 50%;
    .el-dialog__headerbtn:hover .el-dialog__close {
      color: #fff;
    }

    .el-dialog__headerbtn:focus .el-dialog__close {
      color: #fff;
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
        box-shadow: 0 0 0 1px #7697da inset;
      }
    }

    .el-tabs__active-bar {
      background-color: #aebddb;
    }

    .custom-tabs-label {
      font-size: 18px;
      font-weight: bold;
      color: #888;
      margin: 0 20px;
      &:hover {
        color: @theme-color;
      }
    }

    .login-form-item {
      margin-left: 20px;
      margin-right: 20px;
    }

    .el-tabs__content {
      text-align: center;
    }

    .el-tabs__header {
      margin: 0 0 20px;
    }

    .el-tabs__item {
      padding: 0px;
    }

    .el-tabs__item.is-active {
      .custom-tabs-label {
        color: @theme-color;
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

    .bottom-button {
      width: 100px;
    }
  }
</style>
