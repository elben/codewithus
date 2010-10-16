require 'test_helper'

class MergesControllerTest < ActionController::TestCase
  setup do
    @merge = merges(:one)
  end

  test "should get index" do
    get :index
    assert_response :success
    assert_not_nil assigns(:merges)
  end

  test "should get new" do
    get :new
    assert_response :success
  end

  test "should create merge" do
    assert_difference('Merge.count') do
      post :create, :merge => @merge.attributes
    end

    assert_redirected_to merge_path(assigns(:merge))
  end

  test "should show merge" do
    get :show, :id => @merge.to_param
    assert_response :success
  end

  test "should get edit" do
    get :edit, :id => @merge.to_param
    assert_response :success
  end

  test "should update merge" do
    put :update, :id => @merge.to_param, :merge => @merge.attributes
    assert_redirected_to merge_path(assigns(:merge))
  end

  test "should destroy merge" do
    assert_difference('Merge.count', -1) do
      delete :destroy, :id => @merge.to_param
    end

    assert_redirected_to merges_path
  end
end
