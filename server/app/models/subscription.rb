class Subscription < ActiveRecord::Base
  belongs_to :user
  belongs_to :subscribee, :class_name => "User"
end
