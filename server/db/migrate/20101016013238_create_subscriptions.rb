class CreateSubscriptions < ActiveRecord::Migration
  def self.up
    create_table :subscriptions do |t|
      t.integer :subr
      t.integer :sube
      t.integer :latest

      t.timestamps
    end
  end

  def self.down
    drop_table :subscriptions
  end
end
