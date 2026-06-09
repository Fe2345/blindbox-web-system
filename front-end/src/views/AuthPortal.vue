<template>
  <div class="portal-page">
    <section class="portal-panel">
      <div class="portal-heading">
        <p>乐抽盲盒平台</p>
        <h1>选择登录入口</h1>
      </div>

      <div class="portal-grid">
        <article class="portal-card user">
          <div class="card-icon"><User /></div>
          <h2>用户端</h2>
          <p>抽取盲盒、管理资产、换物和查看积分。</p>
          <div class="card-actions">
            <el-button type="primary" @click="go('/user/login')">用户登录</el-button>
            <el-button plain @click="go('/register')">注册用户</el-button>
          </div>
        </article>

        <article class="portal-card admin">
          <div class="card-icon"><Setting /></div>
          <h2>管理员</h2>
          <p>管理商品、盲盒、奖池概率、订单和商家审核。</p>
          <div class="card-actions">
            <el-button type="primary" @click="go('/admin.html#/login')">管理员登录</el-button>
          </div>
          <small>测试账号：admin_p3 / 123456</small>
        </article>

        <article class="portal-card merchant">
          <div class="card-icon"><Shop /></div>
          <h2>商家端</h2>
          <p>提交商品、维护库存、处理发货和查看经营记录。</p>
          <div class="card-actions">
            <el-button type="primary" @click="go('/merchant.html#/login')">商家登录</el-button>
            <el-button plain @click="go('/merchant.html#/register')">注册商家</el-button>
          </div>
          <small>测试账号：merchant_p3 / 123456</small>
        </article>
      </div>
    </section>
  </div>
</template>

<script setup lang="ts">
import { Shop, Setting, User } from '@element-plus/icons-vue'

function go(path: string) {
  window.location.href = path
}
</script>

<style scoped>
.portal-page {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 32px 20px;
  background: #f4f7fb;
}

.portal-panel {
  width: min(1080px, 100%);
}

.portal-heading {
  margin-bottom: 24px;
}

.portal-heading p {
  margin: 0 0 6px;
  color: #606266;
  font-size: 14px;
}

.portal-heading h1 {
  margin: 0;
  color: #1f2d3d;
  font-size: 30px;
  font-weight: 700;
}

.portal-grid {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 16px;
}

.portal-card {
  min-height: 260px;
  padding: 24px;
  border: 1px solid #e4e7ed;
  border-radius: 8px;
  background: #fff;
  display: flex;
  flex-direction: column;
}

.card-icon {
  width: 44px;
  height: 44px;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #fff;
  font-size: 24px;
}

.user .card-icon { background: #409eff; }
.admin .card-icon { background: #303133; }
.merchant .card-icon { background: #67c23a; }

.portal-card h2 {
  margin: 18px 0 8px;
  color: #303133;
  font-size: 20px;
}

.portal-card p {
  min-height: 48px;
  margin: 0 0 18px;
  color: #606266;
  line-height: 1.6;
}

.card-actions {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  margin-top: auto;
}

.portal-card small {
  margin-top: 14px;
  color: #909399;
}

@media (max-width: 860px) {
  .portal-grid {
    grid-template-columns: 1fr;
  }

  .portal-card {
    min-height: auto;
  }
}
</style>
