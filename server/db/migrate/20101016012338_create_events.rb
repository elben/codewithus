class CreateEvents < ActiveRecord::Migration
  def self.up
    create_table :events do |t|
      t.integer :user_id
      t.string :type
      t.integer :data_id

      t.timestamps
    end
  end

  def self.down
    drop_table :events
  end
end
