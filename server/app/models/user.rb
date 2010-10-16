class User < ActiveRecord::Base
  has_many :events

  has_many :subscriptions
  has_many :subscribees, :through => :subscriptions

  #has_many :subscribers, :through => :subcription, :foreign_key => "sube"
  #has_many :subscriptions, :through => :subcription, :foreign_key => "subr"

  #belongs_to :subscribers, :class_name => "Subscription", :foreign_key => "subr"
  #belongs_to :subscriptions, :class_name => "Subscription", :foreign_key => "sube"
end
