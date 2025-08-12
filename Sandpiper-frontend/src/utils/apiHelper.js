import { Notify } from 'quasar'

export async function handleAuthRequest(store, requestFn, router) {
  let response
  try {
    response = await requestFn()
  } catch {
    Notify.create({
      message: 'An unknown error occurred',
      color: 'negative',
    })
    return false
  }

  if (!response.data?.success) {
    Notify.create({
      message: response.data?.message,
      color: 'negative',
    })
    return false
  }

  const { person, access_token, expiry } = response.data

  // Use the store's setAuthData method for consistency
  store.setAuthData({
    user: person,
    accessToken: access_token,
    accessTokenExpiry: expiry,
  })

  router.push('/dashboard')
  return true
}
