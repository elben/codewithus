class RenameSubscriptionColumnsAgain < ActiveRecord::Migration
  def self.up
    rename_column :subscriptions, :subscriber, :subscriber_id
    rename_column :subscriptions, :subscribee, :subscribee_id
  end

  def self.down
    rename_column :subscriptions, :subscribee_id, :subscribee
    rename_column :subscriptions, :subscriber_id, :subscriber
  end
end
