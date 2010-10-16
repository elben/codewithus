class RenameSubscriptionColumns < ActiveRecord::Migration
  def self.up
    rename_column :subscriptions, :subr, :subscriber
    rename_column :subscriptions, :sube, :subscribee
  end

  def self.down
    rename_column :subscriptions, :subscribee, :subr
    rename_column :subscriptions, :subscriber, :sube
  end
end
