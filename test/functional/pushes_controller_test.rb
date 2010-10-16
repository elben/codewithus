require 'test_helper'

class PushesControllerTest < ActionController::TestCase
  setup do
    @push = pushes(:one)
  end

  test "should get index" do
    get :index
    assert_response :success
    assert_not_nil assigns(:pushes)
  end

  test "should get new" do
    get :new
    assert_response :success
  end

  test "should create push" do
    assert_difference('Push.count') do
      post :create, :push => @push.attributes
    end

    assert_redirected_to push_path(assigns(:push))
  end

  test "should show push" do
    get :show, :id => @push.to_param
    assert_response :success
  end

  test "should get edit" do
    get :edit, :id => @push.to_param
    assert_response :success
  end

  test "should update push" do
    put :update, :id => @push.to_param, :push => @push.attributes
    assert_redirected_to push_path(assigns(:push))
  end

  test "should destroy push" do
    assert_difference('Push.count', -1) do
      delete :destroy, :id => @push.to_param
    end

    assert_redirected_to pushes_path
  end
end
