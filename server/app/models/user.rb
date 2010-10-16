class User < ActiveRecord::Base
  has_many :events
  has_many :subrs, :class_name => "Subcription", :foreign_key => "subr"
  has_many :subes, :class_name => "Subcription", :foreign_key => "sube"
end
